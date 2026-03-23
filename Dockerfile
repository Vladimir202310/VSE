FROM apache/airflow:2.7.1-python3.10
USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk wget curl && \
    wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz && \
    tar xzf spark-3.5.0-bin-hadoop3.tgz && \
    mv spark-3.5.0-bin-hadoop3 /opt/spark && \
    rm spark-3.5.0-bin-hadoop3.tgz && \
    curl -L -o /opt/spark/jars/postgresql-42.6.0.jar https://jdbc.postgresql.org/download/postgresql-42.6.0.jar && \
    apt-get clean
ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
USER airflow
RUN pip install pyspark==3.5.0 pandas pyarrow sqlalchemy psycopg2-binary
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
