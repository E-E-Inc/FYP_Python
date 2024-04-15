#FROM ubuntu:latest

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx
    
# Copy the current directory contents into the container at /app
COPY . /FYP_Python

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose any needed ports
EXPOSE 5000
EXPOSE 5001

# Copy specific files into the container
COPY ./src/flask-server.py  ./src/flask-server.py
COPY ./src/image-processing-microservice.py ./src/image-processing-microservice.py
COPY ./start-script.sh start-script.sh

# Make sure the scripts are executable
RUN chmod +x start-script.sh
RUN chmod +x ./src/flask-server.py
RUN chmod +x ./src/image-processing-microservice.py

# Run the script when the container starts
CMD ["./start-script.sh"]