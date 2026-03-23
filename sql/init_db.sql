-- Справочник пользователей
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    user_phone VARCHAR(50)
);

-- Справочник магазинов
CREATE TABLE IF NOT EXISTS stores (
    store_id INT PRIMARY KEY,
    store_address TEXT
);

-- Справочник водителей
CREATE TABLE IF NOT EXISTS drivers (
    driver_id INT PRIMARY KEY,
    driver_phone VARCHAR(50)
);

-- Заказы
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    driver_id INT REFERENCES drivers(driver_id),
    store_id INT REFERENCES stores(store_id),
    address_text TEXT,
    created_at TIMESTAMP,
    paid_at TIMESTAMP,
    delivery_started_at TIMESTAMP,
    delivered_at TIMESTAMP,
    canceled_at TIMESTAMP,
    payment_type VARCHAR(100),
    order_discount INT,
    order_cancellation_reason TEXT,
    delivery_cost INT
);

-- Позиции в заказе
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    item_id INT,
    item_title TEXT,
    item_category TEXT,
    item_quantity INT,
    item_price INT,
    item_discount INT,
    item_canceled_quantity INT,
    item_replaced_id FLOAT
);