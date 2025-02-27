## Dockerfile for FastAPI Backend

# Use official Python image as base
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the dependencies and install them
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY ./ ./

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]