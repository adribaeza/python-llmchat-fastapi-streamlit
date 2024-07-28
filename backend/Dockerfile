# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /api

# Copy the requirements file into the container at /api and install dependencies
COPY requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code into the container at /api
COPY ./api /api

# Copy .env file into the container at /api
COPY .env /api

# Expose the port the api runs in
EXPOSE 8000

# Define environment variable
ENV NAME TinyLlamaLLMApi

# Execute the command to run the app when the container starts
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]