#FROM ubuntu:latest

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /app
COPY . /FYP_Python

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose any needed ports
EXPOSE 5000
EXPOSE 5001

COPY ./src/flask-server.py  flask-server.py
COPY ./src/image-processing-microservice.py image-processing-microservice.py
COPY ./start-script.sh start-script.sh

# Make sure the script is executable
RUN chmod +x start-script.sh
RUN chmod +x flask-server.py
RUN chmod +x image-processing-microservice.py

# Run the script when the container starts
CMD ["./start-script.sh"]