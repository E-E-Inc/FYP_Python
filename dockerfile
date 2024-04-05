# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /fyp-python

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create and activate a virtual environment
RUN python -m venv myenv
RUN . myenv/bin/activate

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start both services
CMD ["sh", "-c", "python ./src/flask-server.py & python ./src/image-processing-microservice.py"]