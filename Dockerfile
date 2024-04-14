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

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["/usr/bin/supervisord"]