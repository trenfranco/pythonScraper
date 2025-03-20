#Use Python 3.11
FROM python:3.11-slim

WORKDIR /app

#Dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    ca-certificates \
    libnss3 \
    libxss1 \
    libx11-xcb1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

#Install google chrome
RUN apt update && apt install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt update && apt install -y google-chrome-stable \
    && ln -sf /usr/bin/google-chrome-stable /usr/bin/google-chrome \
    && rm -rf /var/lib/apt/lists/*

#Install chromedriver
RUN wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.0/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver

#Chrome and chromedriver PATH
ENV CHROME_BINARY="/usr/bin/google-chrome"
ENV PATH="/usr/bin/chromedriver:$PATH"

#Set google cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"

#Copy files
COPY requirements.txt .
COPY scraper.py .
COPY bigqueryUploader.py .
COPY key.json /app/key.json

#Set correct permissions for key.json
RUN chmod 400 /app/key.json

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Run the scraper
CMD ["/usr/local/bin/python", "scraper.py"]
