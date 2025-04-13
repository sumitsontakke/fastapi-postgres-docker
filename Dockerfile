# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set environment variables for your application
ENV PROJECT_NAME="MBdgt"
ENV PROJECT_VERSION="1.0.0"
ENV POSTGRES_HOST="host.docker.internal"
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER="appuser"
ENV POSTGRES_DB="app"
ENV POSTGRES_PASSWORD="supersecretpassword"
ENV SECRET_KEY="skufhoweiu098ye879yih"
ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV DATA_DIRECTORY="/app_data/"

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]