# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /fyp-python

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create a virtual environment and install dependencies
RUN python -m venv myenv && \
    . myenv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start both services
CMD ["sh", "-c", "source myenv/bin/activate && python ./src/flask-server.py & python ./src/image-processing-microservice.py"]