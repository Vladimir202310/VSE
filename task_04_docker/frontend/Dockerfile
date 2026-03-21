FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=120 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# Копируем всё из папки frontend
COPY frontend/ .
CMD ["sh", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true || sleep 3600"]