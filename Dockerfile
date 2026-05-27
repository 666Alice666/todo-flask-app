# Базовый образ
FROM python:3.11-alpine AS builder

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-alpine

# Копирование зависимостей
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# Запуск приложения
CMD ["python", "app.py"]