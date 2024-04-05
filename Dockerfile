# Use an official Python runtime as a parent image
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /app
COPY . /FYP_Python

# Create and activate virtual environment
RUN python -m venv myenv
SHELL ["/bin/bash", "-c"]
RUN source myenv/bin/activate && pip install --no-cache-dir -r requirements.txt


# Expose any needed ports
EXPOSE 5000

# Command to start the server
CMD ["python", "./src/flask-server.py"]