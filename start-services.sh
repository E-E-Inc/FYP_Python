#!/bin/bash
source myenv/bin/activate
python ./src/flask-server.py &
python ./src/image-processing-microservice.py &
wait