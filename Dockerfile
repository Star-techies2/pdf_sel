# Build stage
FROM python:3.11.4-slim as build-stage

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip curl && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.69/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver-linux64.zip -d /app && \
    chmod +x /app/chromedriver-linux64 && \
    rm /tmp/chromedriver-linux64.zip && \
    apt-get install -y --no-install-recommends \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libnspr4 \
        libnss3 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Production stage
FROM python:3.11.4-slim as production-stage

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install updated packages to fix vulnerabilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        krb5-user \
        libexpat1 \
        linux-image-amd64 \
        linux-headers-amd64 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files from the build stage
COPY --from=build-stage /usr/bin/google-chrome /usr/bin/google-chrome
COPY --from=build-stage /app /app

# Set the working directory inside the container
WORKDIR /app

# Expose port 5000
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "app.py"]
