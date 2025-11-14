# Single stage build for simplicity
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies  
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the simple FastAPI application
CMD ["uvicorn", "simple_server:app", "--host", "0.0.0.0", "--port", "8080"]