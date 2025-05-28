FROM python:3.11-slim

# Install deps
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates fonts-liberation \
    libnss3 libatk-bridge2.0-0 libxss1 libasound2 libxshmfence1 \
    libgbm1 libgtk-3-0 libx11-xcb-dev xvfb \
    && rm -rf /var/lib/apt/lists/*

# Setup working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and Chromium
RUN python -m playwright install chromium

# Copy app files
COPY . .

# Run the app
CMD ["python", "app.py"]
