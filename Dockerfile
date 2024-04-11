# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Install required libraries
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx

RUN apt-get update \
    && apt-get install -y libglib2.0-0 libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /FYP_Python
COPY . /FYP_Python

# Create a virtual environment and install Flask and other dependencies
RUN python -m venv myenv && \
    /bin/bash -c "source myenv/bin/activate && pip install flask && pip install --no-cache-dir -r /FYP_Python/requirements.txt"

# Change the permissions of the start.sh script to make it executable
RUN chmod +x /FYP_Python/start.sh

# Expose any needed ports
EXPOSE 5001
EXPOSE 5002

# Run the command to start your application
CMD ["/bin/bash", "-c", "source myenv/bin/activate && /FYP_Python/start.sh"]
