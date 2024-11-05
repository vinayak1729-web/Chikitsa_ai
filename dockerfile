# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port for the application (adjust if needed)
EXPOSE 5000

# Set command to run the application
CMD ["python", "app.py"]
