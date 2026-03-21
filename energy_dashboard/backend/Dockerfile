FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=120 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# Копируем всё из папки backend в контейнер
COPY backend/ .
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 || sleep 3600"]