# Use official Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask torch diffusers transformers accelerate xformers flask-limiter flask-cors

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "server.py"]
