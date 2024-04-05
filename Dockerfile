# Use an official Python runtime as a parent image
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /app
COPY . /FYP_Python

# Create a virtual environment and install dependencies
RUN python -m venv myenv && \
    /bin/bash -c "source myenv/bin/activate" && \
    pip install --no-cache-dir -r requirements.txt

# Expose any needed ports
EXPOSE 5000

# Command to start the server
#CMD ["python", "./src/flask-server.py"]
#CMD ["bash", "-c", "python ./src/flask-server.py && python ./src/image-processing-microservice.py"]
# Run the command to start your application
CMD ["bash", "-c", "source myenv/bin/activate && python ./src/flask-server.py && python ./src/image-processing-microservice.py"]