from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, min, max, sum, avg


JDBC_URL = "jdbc:postgresql://postgres_db:5432/airflow"
JDBC_PROPS = {"user": "airflow", "password": "airflow", "driver": "org.postgresql.Driver"}
SPARK_JAR = "/opt/spark/jars/postgresql-42.6.0.jar"


def _spark():
    spark = SparkSession.builder \
        .appName("DeliveryAnalytics") \
        .config("spark.jars", SPARK_JAR) \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


def build_vitrine_orders():
    spark = _spark()

    df_orders = spark.read.format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "orders") \
        .option("user", JDBC_PROPS["user"]) \
        .option("password", JDBC_PROPS["password"]) \
        .option("driver", JDBC_PROPS["driver"]) \
        .load()

    vitrine_orders = df_orders.groupBy("store_id").agg(
        count("*").alias("total_orders"),
        countDistinct("user_id").alias("unique_customers"),
        min("created_at").alias("first_order"),
        max("created_at").alias("last_order"),
    )

    vitrine_orders.write.mode("overwrite").jdbc(JDBC_URL, "vitrine_orders", properties=JDBC_PROPS)
    spark.stop()


def build_vitrine_items():
    spark = _spark()

    df_items = spark.read.format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "order_items") \
        .option("user", JDBC_PROPS["user"]) \
        .option("password", JDBC_PROPS["password"]) \
        .option("driver", JDBC_PROPS["driver"]) \
        .load()

    vitrine_items = df_items.groupBy("item_category").agg(
        sum(col("item_quantity") * col("item_price")).alias("total_revenue"),
        sum("item_quantity").alias("total_quantity"),
        avg("item_price").alias("avg_price"),
    )

    vitrine_items.write.mode("overwrite").jdbc(JDBC_URL, "vitrine_items", properties=JDBC_PROPS)
    spark.stop()


with DAG(
    dag_id="vitrines_spark_dag",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["spark", "analytics"],
) as dag:

    t_vitrine_orders = PythonOperator(
        task_id="build_vitrine_orders",
        python_callable=build_vitrine_orders,
    )

    t_vitrine_items = PythonOperator(
        task_id="build_vitrine_items",
        python_callable=build_vitrine_items,
    )

    t_vitrine_orders >> t_vitrine_items