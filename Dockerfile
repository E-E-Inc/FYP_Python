# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /app
COPY . /FYP_Python

# Install Flask
RUN pip install flask

# Install Flask-CORS
RUN pip install -U flask-cors

# Install mysql-connector-python
RUN pip install mysql-connector-python

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose any needed ports
EXPOSE 5000
EXPOSE 5001

# Run the command to start your application
CMD ["python", "./src/flask-server.py", "&", "python ./src/image-processing-microservice.py"]