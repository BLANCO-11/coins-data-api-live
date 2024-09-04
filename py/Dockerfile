# Start with a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary system packages
RUN apt-get update --fix-missing && apt-get install -y \
    wget \
    unzip \
    curl \
    gcc \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxi6 \
    libgbm-dev \
    libpq-dev \
    libxkbcommon-x11-0 \
    nano \
    && rm -rf /var/lib/apt/lists/*
    
    # gnupg2 \

RUN apt-get update && apt-get install -y gnupg2

# Install Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add   \
    && bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" \
    && apt -y update \
    && apt -y install google-chrome-stable

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+\.\d+") \
    && wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && rm chromedriver-linux64.zip \
    && mv chromedriver-linux64 /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY scrapper.py .

# Specify the command to run your Python script
CMD ["python", "scrapper.py", "10"]
