FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg libglib2.0-0 libnss3 libgconf-2-4 \
    libfontconfig1 libxss1 libappindicator1 libasound2 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdbus-1-3 libgtk-3-0 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Установка Chrome 122
RUN wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux/x64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm chrome-linux64.zip

# Установка ChromeDriver 122
RUN wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# Установка Python-библиотек
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
