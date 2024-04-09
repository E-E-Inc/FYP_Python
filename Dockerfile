# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /app
COPY . /FYP_Python

# Install Flask, supervisor and create a virtual environment, then install dependencies
RUN python -m venv myenv && \
    /bin/bash -c "source myenv/bin/activate && pip install flask supervisor && pip install --no-cache-dir -r requirements.txt"

# Expose any needed ports
EXPOSE 5000
EXPOSE 5001

# Create a supervisord.conf file
RUN echo "[supervisord]\nnodaemon=true\n\n[program:flask-server]\ncommand=python ./src/flask-server.py\n\n[program:image-processing-microservice]\ncommand=python ./src/image-processing-microservice.py" > supervisord.conf

# Run supervisord to start your applications
CMD ["bash", "-c", "source myenv/bin/activate && supervisord -c supervisord.conf"]