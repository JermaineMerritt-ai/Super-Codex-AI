FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir Flask==3.0.0 jsonschema waitress

# Copy the entire project structure
COPY . .

# Create required directories
RUN mkdir -p /app/storage/ledger /app/storage/replays /app/storage/annals

# Set working directory to the API package
WORKDIR /app/packages/api

# Expose port
EXPOSE 8097

# Use the original app.py with waitress
CMD ["python", "-m", "waitress", "--host=0.0.0.0", "--port=8097", "app:app"]