CREATE TABLE IF NOT EXISTS users (
  user_id     BIGINT PRIMARY KEY,
  user_phone  TEXT
);

CREATE TABLE IF NOT EXISTS drivers (
  driver_id    BIGINT PRIMARY KEY,
  driver_phone TEXT
);

CREATE TABLE IF NOT EXISTS stores (
  store_id      BIGINT PRIMARY KEY,
  store_address TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  order_id        BIGINT PRIMARY KEY,
  user_id         BIGINT REFERENCES users(user_id),
  store_id        BIGINT REFERENCES stores(store_id),
  address_text    TEXT,
  created_at      TIMESTAMP,
  paid_at         TIMESTAMP,
  delivery_started_at TIMESTAMP,
  delivered_at    TIMESTAMP,
  canceled_at     TIMESTAMP,
  payment_type    TEXT,
  order_discount  NUMERIC,
  delivery_cost   NUMERIC
);

CREATE TABLE IF NOT EXISTS order_items (
  order_id               BIGINT REFERENCES orders(order_id),
  item_id                BIGINT,
  item_title             TEXT,
  item_category          TEXT,
  item_quantity          NUMERIC,
  item_price             NUMERIC,
  item_discount          NUMERIC,
  item_canceled_quantity NUMERIC,
  item_replaced_id       BIGINT,
  PRIMARY KEY (order_id, item_id)
);