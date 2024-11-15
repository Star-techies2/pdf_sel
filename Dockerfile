# Use the official Python image from the Docker Hub
FROM python:3.11.4-slim

# Set environment variable to ensure Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip curl && \
    wget -O /tmp/google-chrome-stable_130.0.6723.117-1_amd64.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_130.0.6723.117-1_amd64.deb && \
    dpkg -i /tmp/google-chrome-stable_130.0.6723.117-1_amd64.deb || apt-get -f install -y && \
    rm /tmp/google-chrome-stable_130.0.6723.117-1_amd64.deb && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/130.0.6723.117/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
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
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "app.py"]
