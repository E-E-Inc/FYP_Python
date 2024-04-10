# Activate the virtual environment
source /FYP_Python/myenv/bin/activate

# Run Flask server
python /FYP_Python/src/flask-server.py &

# Run image processing microservice
python /FYP_Python/src/image-processing-microservice.py &

# Keep container running
tail -f /dev/null
