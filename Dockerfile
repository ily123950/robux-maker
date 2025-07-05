FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg libglib2.0-0 libnss3 libgconf-2-4 \
    libfontconfig1 libxss1 libappindicator1 libasound2 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdbus-1-3 libgtk-3-0 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Установка Google Chrome (v124)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome*.deb || apt-get -fy install && \
    rm google-chrome*.deb

# Установка ChromeDriver (v124.0.6367.91 — соответствует Chrome 124)
RUN wget -q https://chromedriver.storage.googleapis.com/124.0.6367.91/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Установка Python зависимостей
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
