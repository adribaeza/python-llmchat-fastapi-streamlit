# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the app 
COPY ./app /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env file into the container at /app
COPY .env /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

ENV RUNNING_IN_DOCKER=true

# Run app.py when the container launches
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
