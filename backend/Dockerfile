FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY . .

# Make start script executable
RUN chmod +x /app/start.sh

EXPOSE 8000

# Use bash to run the script
CMD ["bash", "/app/start.sh"]