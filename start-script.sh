#!/bin/bash

python3 ./src/flask-server.py &

# Start the second process
# python3 ./src/image-processing-microservice.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?