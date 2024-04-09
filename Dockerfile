# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /FYP_Python
COPY . /FYP_Python

# Create a virtual environment and install dependencies
RUN python -m venv myenv && \
    /bin/bash -c "source myenv/bin/activate && \
                  pip install --no-cache-dir -r requirements.txt && \
                  pip install flask"

# Expose any needed ports
EXPOSE 5000
EXPOSE 5001

# Start the application
CMD /bin/bash -c "source myenv/bin/activate && \
                  python ./src/flask-server.py & python ./src/image-processing-microservice.py"
