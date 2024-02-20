from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from FoodRecognition import IdentifyFoodYolo

from flask_bcrypt import Bcrypt  # Importing Bcrypt for password hashing
import jwt  # Importing JWT for token-based authentication
import datetime
import mysql.connector  # Importing MySQL connector for database interaction
import secrets

app = Flask(__name__)
bcrypt = Bcrypt(app)  # Creating a Bcrypt instance for password hashing

secret_key = secrets.token_hex(32) 

CORS(app)
IMAGES_DIR = os.path.abspath(".\\src\\Images\\")
app.config['SECRET_KEY'] = os.urandom(24)
# MySQL Connection
db = mysql.connector.connect(
     host="fyp-db-24.cjyypjykw7a3.us-east-1.rds.amazonaws.com",  # MySQL host
    port="3306",  # MySQL port
    user="Marbles7558",  # MySQL user
    password="UxJ2r$xTT",  # MySQL password
    database="mydb" 
)

# Global variable to store the image temporarily
temp_image = None

# Global variable to store food data 
food_data = None

# Handle POST request to '/upload' endpoint for uploading an image
@app.route('/upload', methods=['POST'])
def upload():

    global temp_image

    # Get the file from post request
    file = request.files['file']
    
    # TODO: Process the image asynchronously using a message queue
    # For now just call the function directly
    if file:
        # Secure the filename to avoid unsafe characters
        filename = secure_filename(file.filename)
       
        # Save the file to a temporary location to be processed
        temp_path = os.path.join(IMAGES_DIR, filename)
        file.save(temp_path)

        # Store the image path temporarily
        temp_image = temp_path
        

    # Return the result
    if file.filename == '':
        response = {'status': 'error', 'message': 'Error processing image'}
    else:
        response = {'status': 'success', 'message': 'File uploaded successfully'}

    return json.dumps(response)

@app.route('/process', methods=['POST'])
def process():

    # takes in the temp_image
    global temp_image

    # Gets the portion size
    data = request.get_json()
    portion_Size = data.get('portionSize')

    # If there is an image
    if temp_image:
        # Call the function to process the image
        result = IdentifyFoodYolo.Identification(temp_image, portion_Size)

        # Remove the temporary file
        os.remove(temp_image)
        temp_image = None

        return jsonify(result=result)
    else:
        response = {'status': 'error', 'message': 'No image uploaded'}

    return json.dumps(response)

@app.route('/getFoodData', methods=['GET'])
def get_food_data():
    # Referencing the global variable 
    global food_data
    print("food_data: ", food_data)

    # If there is a value in the food data
    if food_data:
        return jsonify(food_data)
    else:
        response  = {'status': 'error', 'message': 'No food data available'}

    return json.dumps(response)

# Registration Endpoint 
@app.route('/register', methods=['POST'])
def registeration():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = db.cursor()
        cursor.execute("INSERT INTO Users (email, password) VALUES (%s, %s)", (email, hashed_password))
        db.commit()
        cursor.close()
        print(f"here")

        return jsonify({'message': 'User registered successfully'})
        

    except Exception as e:
        logging.error(f"Registration failed: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

# Run the server in debug mode - 'python flask-server.py'
if __name__ == '__main__':
    app.run(debug=True)