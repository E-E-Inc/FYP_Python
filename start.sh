#!/bin/bash
gunicorn src/flask-server:app &
gunicorn src/image-processing-microservice:app &