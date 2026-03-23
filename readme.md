# Итоговый проект: Аналитика доставок (Airflow + PySpark + PostgreSQL)

## Запуск

1. Убедись, что Docker Desktop запущен
2. Клонируй репозиторий в папку `final_project/`
3. Помести исходные parquet-файлы в `./team_11/`
4. Выполни команды:

```bash
docker compose up -d --build
docker exec airflow_webserver airflow db init
docker compose restart airflow-scheduler


Необходимо открыть интерфейсы:
Airflow UI: http://localhost:8080 (admin/admin)
pgAdmin: http://localhost:5050 (admin@admin.com / admin)
PostgreSQL: localhost:5432 (airflow/airflow)



Проверка работы

Airflow → normalize_deliveries_data → Clear → Trigger DAG
Airflow → vitrines_spark_dag → Clear → Trigger DAG

Проверка данных
docker exec postgres_db psql -U airflow -d airflow -c "SELECT * FROM vitrine_items ORDER BY total_revenue DESC LIMIT 5;"

Архитектура

PostgreSQL (3NF: users, stores, orders, order_items)
Airflow (2 DAG: нормализация + PySpark-витрины)
PySpark (JDBC → агрегация → JDBC)
pgAdmin (управление БД)

Результат
Витрина категорий товаров (топ-5 по выручке):

Мясо: ~2.33 млрд руб.
Овощи: ~2.15 млрд руб.
Фрукты: ~1.63 млрд руб.

Схема БД и DDL-скрипты: final_project_report.pdf

