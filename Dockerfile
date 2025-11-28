  FROM python:3.13.19-slim

WORKDIR /app

# Копируем только requirements сначала для кэширования
COPY requirements.txt .

# Устанавливаем зависимости с оптимизацией памяти
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Запускаем бота
CMD ["python", "app.py"]
