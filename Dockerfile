# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /FYP_Python

# Copy the current directory contents into the container at /FYP_Python
COPY . /FYP_Python

# Install Flask and create a virtual environment, then install dependencies
RUN python -m venv myenv && \
    /FYP_Python/myenv/bin/pip install flask && \
    /FYP_Python/myenv/bin/pip install --no-cache-dir -r /FYP_Python/requirements.txt

# Expose any needed ports
EXPOSE 5000
EXPOSE 5001

# Run the command to start your application
CMD ["/bin/bash", "/FYP_Python/start.sh"]
