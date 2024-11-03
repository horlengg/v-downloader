# # Use the official Python 3.8 slim image as the base image
# FROM python:3.8-slim

# # Set the working directory within the container
# WORKDIR /app

# COPY requirements.txt /app/requirements.txt


# # Upgrade pip and install Python dependencies
# RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# COPY . /app

# # Expose port 5000 for the Flask application
# EXPOSE 5000

# # Define the command to run the Flask application using Gunicorn
# CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port that the app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]
