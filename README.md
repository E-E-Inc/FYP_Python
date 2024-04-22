## Overview 
This repository contains the backend code for the Food Logix app, including both the main service and the food detection microservice. 

## Setting Up the Environment
To run this project, we recommend creating a Python virtual environment and installing the required packages.

### Create a virtual environment (optional but recommended):
   `python -m venv myenv`
###  Activate the Environment 
`myenv\Scripts\activate`
###  Install project dependencies 
`pip install -r requirements.txt`

### Start the server
`python .\src\flask-server.py`

### Start the microservice
`python ./src/image-processing-microservice.py`
