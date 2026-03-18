# Домашняя работа #5

import psycopg2
import pandas as pd
import warnings

# Подавление всех предупреждений
warnings.filterwarnings('ignore')


# Параметры подключения к БД
DB_CONFIG = {
    'host': 'rc1b-7ng6ih3jte3824x8.mdb.yandexcloud.net',
    'port': 6432,
    'dbname': 'demo',
    'user': 'student',
    'password': 'student!'
}


def execute_task(conn, task_num, description, query):
    """Выполнение задания и вывод результатов"""
    print(f"\n{'='*80}")
    print(f"Задание {task_num}: {description}")
    print(f"{'='*80}")
    
    try:
        df = pd.read_sql_query(query, conn)
        print(f"Найдено записей: {len(df)}\n")
        print(df.head(10))
        
        if len(df) > 10:
            print(f"\n... (показаны первые 10 из {len(df)} строк)")
        
        return df
    except Exception as e:
        print(f"\n✗ Ошибка выполнения запроса: {e}")
        return pd.DataFrame()


def main():
    """Главная функция"""
    
    print("="*80)
    print("ДЗ №5, SQL, Часть 1 и Часть 2")
    print("БД: demo (PostgreSQL)")
    print("="*80)
    
    conn = None
    
    try:
        # Подключение к БД
        print("\nПодключение к БД...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Успешно подключено\n")
        
        # ========== ЧАСТЬ 1 ==========
        print("\n" + "="*80)
        print("ЧАСТЬ 1")
        print("="*80)
        
        # Задание 1: Вывести всю информацию из таблицы ticket_flights
        query_1 = """
        SELECT * 
        FROM booking.ticket_flights;
        """
        execute_task(conn, 1, "Вывести всю информацию из таблицы ticket_flights", query_1)
        
        # Задание 2: Вывести номера билетов и их стоимость из таблицы ticket_flights, где класс бронирования Business
        query_2 = """
        SELECT ticket_no, amount 
        FROM booking.ticket_flights 
        WHERE fare_conditions = 'Business';
        """
        execute_task(conn, 2, "Вывести номера билетов и их стоимость, где класс бронирования Business", query_2)
        
        # Задание 3: Вывести коды аэропортов, которые находятся во временной зоне Europe/Moscow
        query_3 = """
        SELECT airport_code 
        FROM booking.airports_data 
        WHERE timezone = 'Europe/Moscow';
        """
        execute_task(conn, 3, "Вывести коды аэропортов во временной зоне Europe/Moscow", query_3)
        
        # Задание 4: Вывести всю информацию из таблицы flights, где номер полета является «PG0216»
        query_4 = """
        SELECT * 
        FROM booking.flights 
        WHERE flight_no = 'PG0216';
        """
        execute_task(conn, 4, "Вывести всю информацию о полете PG0216", query_4)
        
        # Задание 5: Вывести из таблицы flights все рейсы из Домодедово в Пулково
        query_5 = """
        SELECT * 
        FROM booking.flights 
        WHERE departure_airport = 'DME' 
          AND arrival_airport = 'LED';
        """
        execute_task(conn, 5, "Вывести все рейсы из Домодедово (DME) в Пулково (LED)", query_5)
        
        # Задание 6: Вывести из таблицы flights рейсы, вылет которых был запланирован в интервале с 10 февраля 2017 по 10 апреля 2017
        query_6 = """
        SELECT * 
        FROM booking.flights 
        WHERE scheduled_departure >= '2017-02-10 00:00:00' 
          AND scheduled_departure <= '2017-04-10 23:59:59';
        """
        execute_task(conn, 6, "Вывести рейсы с вылетом в интервале 10.02.2017 - 10.04.2017", query_6)
        
        # Задание 7: Вывести названия моделей самолётов на английском языке, дальность полета которых менее 5000 км
        query_7 = """
        SELECT model->>'en' AS model_english, range
        FROM booking.aircrafts_data 
        WHERE range < 5000;
        """
        execute_task(conn, 7, "Вывести названия самолётов (англ.) с дальностью < 5000 км", query_7)
        
        # Задание 8: Вывести всю информацию из таблицы tickets, отсортированную по колонке passenger_name в обратном порядке и ограничением выборки в 100 записей
        query_8 = """
        SELECT * 
        FROM booking.tickets 
        ORDER BY passenger_name DESC 
        LIMIT 100;
        """
        execute_task(conn, 8, "Вывести билеты, отсортированные по passenger_name DESC, LIMIT 100", query_8)
        
        # Задание 9: Вывести из таблицы tickets поля ticket_no и passenger_name, где имя пассажира VIKTORIYA SMIRNOVA
        query_9 = """
        SELECT ticket_no, passenger_name 
        FROM booking.tickets 
        WHERE passenger_name = 'VIKTORIYA SMIRNOVA';
        """
        execute_task(conn, 9, "Вывести билеты пассажира VIKTORIYA SMIRNOVA", query_9)
        
        # Задание 10: Вывести из таблицы tickets имена и фамилии всех пассажиров, фамилии которых заканчиваются на «NOV» или «OVA», отсортировав их сначала по номеру билета, а затем по имени пассажира в обратном порядке
        query_10 = """
        SELECT ticket_no, passenger_name 
        FROM booking.tickets 
        WHERE passenger_name LIKE '% NOV' 
           OR passenger_name LIKE '% OVA' 
        ORDER BY ticket_no ASC, passenger_name DESC;
        """
        execute_task(conn, 10, "Вывести пассажиров с фамилиями на NOV/OVA, сортировка по ticket_no, passenger_name DESC", query_10)
        
        # ========== ЧАСТЬ 2 ==========
        print("\n" + "="*80)
        print("ЧАСТЬ 2")
        print("="*80)
        
        # Задание 1: Подсчитать общее количество самолетов в таблице aircrafts_data
        query_11 = """
        SELECT COUNT(*) AS total_aircrafts 
        FROM booking.aircrafts_data;
        """
        execute_task(conn, 11, "Подсчитать общее количество самолетов", query_11)
        
        # Задание 2: Вычислить среднюю дальность полета самолетов
        query_12 = """
        SELECT AVG(range) AS avg_range 
        FROM booking.aircrafts_data;
        """
        execute_task(conn, 12, "Вычислить среднюю дальность полета самолетов", query_12)
        
        # Задание 3: Найти максимальную дальность полета среди всех самолетов
        query_13 = """
        SELECT MAX(range) AS max_range 
        FROM booking.aircrafts_data;
        """
        execute_task(conn, 13, "Найти максимальную дальность полета", query_13)
        
        # Задание 4: Подсчитать общее количество аэропортов в таблице airports_data
        query_14 = """
        SELECT COUNT(*) AS total_airports 
        FROM booking.airports_data;
        """
        execute_task(conn, 14, "Подсчитать общее количество аэропортов", query_14)
        
        # Задание 5: Вычислить среднюю, медиану и моду стоимости бронирования
        query_15 = """
        SELECT 
            AVG(amount) AS avg_amount,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_amount,
            MODE() WITHIN GROUP (ORDER BY amount) AS mode_amount
        FROM booking.ticket_flights;
        """
        execute_task(conn, 15, "Вычислить среднюю, медиану и моду стоимости бронирования", query_15)
        
        # Задание 6: Найти первые пять самых дорогих бронирований
        query_16 = """
        SELECT * 
        FROM booking.bookings 
        ORDER BY total_amount DESC 
        LIMIT 5;
        """
        execute_task(conn, 16, "Найти первые пять самых дорогих бронирований", query_16)
        
        # Задание 7: Подсчитать общее количество посадочных талонов
        query_17 = """
        SELECT COUNT(*) AS total_boarding_passes 
        FROM booking.boarding_passes;
        """
        execute_task(conn, 17, "Подсчитать общее количество посадочных талонов", query_17)
        
        # Задание 8: Вычислить суммарную стоимость всех билетов класса комфорт
        query_18 = """
        SELECT SUM(amount) AS total_comfort_amount 
        FROM booking.ticket_flights 
        WHERE fare_conditions = 'Comfort';
        """
        execute_task(conn, 18, "Вычислить суммарную стоимость всех билетов класса комфорт", query_18)
        
        # Задание 9: Найти первый и последний рейсы
        query_19 = """
        (SELECT 'Первый рейс' AS flight_type, * 
         FROM booking.flights 
         ORDER BY scheduled_departure ASC 
         LIMIT 1)
        UNION ALL
        (SELECT 'Последний рейс' AS flight_type, * 
         FROM booking.flights 
         ORDER BY scheduled_departure DESC 
         LIMIT 1);
        """
        execute_task(conn, 19, "Найти первый и последний рейсы", query_19)
        
        # Задание 10: Найти среднюю стоимость билетов по классам обслуживания
        query_20 = """
        SELECT 
            fare_conditions AS class, 
            AVG(amount) AS avg_amount,
            COUNT(*) AS ticket_count
        FROM booking.ticket_flights 
        GROUP BY fare_conditions 
        ORDER BY avg_amount DESC;
        """
        execute_task(conn, 20, "Найти среднюю стоимость билетов по классам обслуживания", query_20)
        
        print("\n" + "="*80)
        print("✓ Все задания (Часть 1 и Часть 2) выполнены успешно!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Критическая ошибка: {e}")
    
    finally:
        if conn:
            conn.close()
            print("\n✓ Соединение с БД закрыто")


if __name__ == "__main__":
    main()