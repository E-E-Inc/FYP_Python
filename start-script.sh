#!/bin/bash

# Start the first process
./src/flask-server.py &

# Start the second process
./src/image-processing-microservice.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?