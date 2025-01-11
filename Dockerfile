# Используем базовый образ с Python
FROM python:3.11-slim

# Устанавливаем необходимые пакеты для работы с Chrome и Selenium
RUN apt-get update && apt-get install -y \
    wget curl unzip \
    libx11-dev libx11-6 libxcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libgbm-dev libxss1 libappindicator3-1 \
    libxtst6 chromium chromium-driver

# Устанавливаем selenium и flask
RUN pip install selenium flask

# Указываем рабочую директорию для копирования файлов проекта
WORKDIR /usr/src/app

# Копируем файлы проекта в контейнер
COPY . .

# Открываем порт, который будет слушать Flask сервер
EXPOSE 10000

# Указываем команду для запуска скрипта
CMD ["python", "main.py"]
