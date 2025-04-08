FROM python:3.12-slim

# Установка системных зависимостей и uv
RUN apt-get update && apt-get install -y gcc python3-dev && \
    pip install --no-cache-dir uv && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости отдельно для кэширования
COPY pyproject.toml README.md ./

# Установка зависимостей в системное окружение:cite[2]
RUN uv pip install . --system --no-cache-dir

# Копируем исходный код
COPY . .

# 7. Открываем порт приложения
EXPOSE 8000

# 8. Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]