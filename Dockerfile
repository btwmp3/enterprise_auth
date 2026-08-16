FROM python:3.11-slim

# Отключаем буферизацию вывода Python (чтобы логи сразу летели в консоль)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

EXPOSE 8000