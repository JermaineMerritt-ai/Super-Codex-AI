FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir Flask==3.0.0 jsonschema waitress

# Copy application files
COPY . .

# Create required directories and dummy structure for Docker
RUN mkdir -p /app/storage/ledger /app/storage/replays /app/storage/annals /app/artifacts/schemas

# Copy schemas if they exist
RUN if [ -d "../../../artifacts" ]; then cp -r ../../../artifacts/* /app/artifacts/; fi || true

# Create a minimal app.py that works in Docker
COPY app.py /app/app.py

# Expose port
EXPOSE 8095

# Use the Docker-specific Flask app
CMD ["python", "docker_app.py"]