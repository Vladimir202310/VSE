-- ============================================================
-- SQL Tasks - Part 1 and Part 2
-- ============================================================

\echo '================================================================================'
\echo 'PART 1'
\echo '================================================================================'
\echo ''

\echo 'Task 1: Select all from ticket_flights'
SELECT * FROM booking.ticket_flights LIMIT 100;
\echo ''

\echo 'Task 2: Ticket numbers and amounts for Business class'
SELECT ticket_no, amount FROM booking.ticket_flights WHERE fare_conditions = 'Business' LIMIT 100;
\echo ''

\echo 'Task 3: Airport codes in Europe/Moscow timezone'
SELECT airport_code FROM booking.airports_data WHERE timezone = 'Europe/Moscow' LIMIT 100;
\echo ''

\echo 'Task 4: All flights with flight_no = PG0216'
SELECT * FROM booking.flights WHERE flight_no = 'PG0216' LIMIT 100;
\echo ''

\echo 'Task 5: Flights from DME to LED'
SELECT * FROM booking.flights WHERE departure_airport = 'DME' AND arrival_airport = 'LED' LIMIT 100;
\echo ''

\echo 'Task 6: Flights scheduled between 2017-02-10 and 2017-04-10'
SELECT * FROM booking.flights WHERE scheduled_departure >= '2017-02-10 00:00:00' AND scheduled_departure <= '2017-04-10 23:59:59' LIMIT 100;
\echo ''

\echo 'Task 7: Aircraft models (English) with range < 5000 km'
SELECT model->>'en' AS model_english, range FROM booking.aircrafts_data WHERE range < 5000 LIMIT 100;
\echo ''

\echo 'Task 8: Tickets ordered by passenger_name DESC'
SELECT * FROM booking.tickets ORDER BY passenger_name DESC LIMIT 100;
\echo ''

\echo 'Task 9: Tickets for VIKTORIYA SMIRNOVA'
SELECT ticket_no, passenger_name FROM booking.tickets WHERE passenger_name = 'VIKTORIYA SMIRNOVA' LIMIT 100;
\echo ''

\echo 'Task 10: Passengers with surnames ending NOV or OVA'
SELECT ticket_no, passenger_name FROM booking.tickets WHERE passenger_name LIKE '% NOV' OR passenger_name LIKE '% OVA' ORDER BY ticket_no ASC, passenger_name DESC LIMIT 100;
\echo ''

\echo '================================================================================'
\echo 'PART 2'
\echo '================================================================================'
\echo ''

\echo 'Task 11: Total number of aircrafts'
SELECT COUNT(*) AS total_aircrafts FROM booking.aircrafts_data;
\echo ''

\echo 'Task 12: Average aircraft range'
SELECT AVG(range) AS avg_range FROM booking.aircrafts_data;
\echo ''

\echo 'Task 13: Maximum aircraft range'
SELECT MAX(range) AS max_range FROM booking.aircrafts_data;
\echo ''

\echo 'Task 14: Total number of airports'
SELECT COUNT(*) AS total_airports FROM booking.airports_data;
\echo ''

\echo 'Task 15: Average, median and mode of ticket amounts'
SELECT AVG(amount) AS avg_amount, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_amount, MODE() WITHIN GROUP (ORDER BY amount) AS mode_amount FROM booking.ticket_flights;
\echo ''

\echo 'Task 16: Top 5 most expensive bookings'
SELECT * FROM booking.bookings ORDER BY total_amount DESC LIMIT 5;
\echo ''

\echo 'Task 17: Total boarding passes'
SELECT COUNT(*) AS total_boarding_passes FROM booking.boarding_passes;
\echo ''

\echo 'Task 18: Total amount for Comfort class'
SELECT SUM(amount) AS total_comfort_amount FROM booking.ticket_flights WHERE fare_conditions = 'Comfort';
\echo ''

\echo 'Task 19: First and last flights'
(SELECT 'First' AS flight_type, * FROM booking.flights ORDER BY scheduled_departure ASC LIMIT 1) UNION ALL (SELECT 'Last' AS flight_type, * FROM booking.flights ORDER BY scheduled_departure DESC LIMIT 1);
\echo ''

\echo 'Task 20: Average amount by fare class'
SELECT fare_conditions AS class, AVG(amount) AS avg_amount, COUNT(*) AS ticket_count FROM booking.ticket_flights GROUP BY fare_conditions ORDER BY avg_amount DESC;
\echo ''

\echo '================================================================================'
\echo 'ALL TASKS COMPLETED'
\echo '================================================================================'
