from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# Функция для нормализации и загрузки данных
def extract_and_load():
    import glob
    import pandas as pd
    from sqlalchemy import create_engine
    
    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres_db:5432/airflow')
    
    # Шаг 1: Полная очистка всех таблиц (идемпотентность)
    print("Очистка таблиц...")
    with engine.begin() as conn:
        conn.exec_driver_sql("DROP TABLE IF EXISTS order_items, orders, users, drivers, stores, couriers CASCADE;")
        conn.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY, user_phone TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS stores (
                store_id INTEGER PRIMARY KEY, store_address TEXT
            );
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(user_id),
                store_id INTEGER REFERENCES stores(store_id), address_text TEXT, created_at TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS order_items (
                order_id INTEGER REFERENCES orders(order_id), item_id INTEGER,
                item_title TEXT, item_category TEXT, item_quantity INTEGER, item_price DECIMAL,
                PRIMARY KEY (order_id, item_id)
            );
        """)
    
    # Шаг 2: Загрузка parquet файлов
    path = '/opt/airflow/data/team_11/*.parquet'
    all_files = glob.glob(path)
    print(f"Найдено файлов: {len(all_files)}")
    
    df = pd.concat((pd.read_parquet(f) for f in all_files), ignore_index=True)
    print(f"Всего строк загружено: {len(df)}")
    
    # Шаг 3: Загрузка пользователей (уникальные)
    users = df[['user_id', 'user_phone']].drop_duplicates(subset=['user_id'])
    users.to_sql('users', engine, if_exists='append', index=False)
    print(f"Пользователи: {len(users)}")
    
    # Шаг 4: Загрузка магазинов (уникальные)
    stores = df[['store_id', 'store_address']].drop_duplicates(subset=['store_id'])
    stores.to_sql('stores', engine, if_exists='append', index=False)
    print(f"Магазины: {len(stores)}")
    
    # Шаг 5: Загрузка заказов (уникальные)
    orders = df[['order_id', 'user_id', 'store_id', 'address_text', 'created_at']].drop_duplicates(subset=['order_id'])
    orders.to_sql('orders', engine, if_exists='append', index=False)
    print(f"Заказы: {len(orders)}")
    
    # Шаг 6: Загрузка товаров (защита от дублей)
    print("Подготовка товаров (drop_duplicates)...")
    
    # Берем нужные колонки и удаляем полные дубликаты строк
    items_cols = ['order_id', 'item_id', 'item_title', 'item_category', 'item_quantity', 'item_price']
    items = df[items_cols].drop_duplicates(subset=['order_id', 'item_id'])
    
    # Гарантируем типы данных
    items['item_quantity'] = items['item_quantity'].astype(int)
    items['item_price'] = items['item_price'].astype(float)
    
    # Загружаем пачками по 10 000 строк (chunksize), чтобы не перегружать память
    items.to_sql('order_items', engine, if_exists='append', index=False, chunksize=10000)
    print(f"✅ Товары загружены: {len(items)} строк")

# Объявление DAG
with DAG(
    'normalize_deliveries_data',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    template_searchpath=['/opt/airflow/sql']
) as dag:

    # Задача 1: Создание таблиц (DDL)
    # Скрипт ddl.sql должен лежать в папке dags/sql/ или быть доступен по пути
    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_default",
        sql="ddl.sql" 
    )

    # Задача 2: Загрузка данных
    load_task = PythonOperator(
        task_id='extract_and_normalize_parquet',
        python_callable=extract_and_load
    )

    # Устанавливаем зависимость: сначала таблицы, потом данные
    create_tables >> load_task