# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные среды для Python
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY . /app/

# Команда для запуска вашего бота
CMD ["python", "bot.py"]
