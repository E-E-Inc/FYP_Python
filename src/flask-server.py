from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from FoodRecognition import IdentifyFoodYolo, getCalories, getNutrientInfo
import mysql.connector  # Importing MySQL connector for database interaction
import secrets
import logging
import hashlib
from dotenv import load_dotenv
from datetime import datetime
import requests
app = Flask(__name__)
load_dotenv()

secret_key = secrets.token_hex(32) 

MICROSERVICE_URL = 'http://localhost:5001'  

CORS(app)
IMAGES_DIR = os.path.abspath(".\\src\\Images\\")

app.config['SECRET_KEY'] = os.urandom(24)

# MySQL Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"), 
    user=os.getenv("DB_USER"),  
    password=os.getenv("DB_PASSWORD"), 
    database=os.getenv("DB_NAME")
)

# Global variable to store the image temporarily
temp_image = None

# Global variable for user id
userid = None

# Global variable to store food data 
food_data = None

# food_name = None;
# portion = None#

# Handle POST request to '/upload' endpoint for uploading an image
@app.route('/image_upload', methods=['POST'])
def image_upload():

    print(session.get('uid'))

    # Get the file from post request
    file = request.files['file']
    print("File", file)

    if not file:
        return jsonify({'error':'no file part'})
    
    try:
        url= f'{MICROSERVICE_URL}/upload'
        files = {'file': file}
        response = requests.post(url, files=files)
        print(response)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            print("here")
            return jsonify({'error': 'upload failed'})

    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'})

@app.route('/image_process', methods=['POST'])
def image_process():

    # Gets the portion size
    data = request.get_json()
    print("in main flask /image_process > ",data)
    if not data:
        return jsonify({'error': 'No data provided'})
    
    # Add the user ID to the data
    data['uid'] = userid

    try:
        url= f'{MICROSERVICE_URL}/process'
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'processing failed'})
    
    except Exception as e:
        return jsonify({'error': f'processing failed: {str(e)}'})
   
@app.route('/image_process_manually', methods=['POST'])
def image_process_manually():

    global userid

    # Gets the portion size
    data = request.get_json()
    print("in main flask /image_process_manually > ",data)

    # Extract food name and portion size from the JSON data
    food_name = data.get('foodName')
    portion_size = data.get('portion')
    
    if not data:
        return jsonify({'error': 'No data provided'})
    
    # Add the user ID to the data
    data['uid'] = userid
   
    try:
        url= f'{MICROSERVICE_URL}/process_manually'
        payload = {
            'foodName': food_name,
            'portion': portion_size,
            'uid': userid
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'processing failed'})
    
    except Exception as e:
        return jsonify({'error': f'processing failed: {str(e)}'})
   

# Registration Endpoint 
@app.route('/register', methods=['POST'])
def registeration():
    try:
        # Get data from the request
        data = request.get_json()

        # Get email and password
        email = data.get('email')
        password = data.get('password')

        # If there is no email or password entered, throw an error
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
          # Email validation
        if '@' not in email or '.com' not in email:
            return jsonify({'error': 'Invalid format for email'}), 400
        
        # Password validation
        if len(password) < 6:
            return jsonify({'error':'Password must have'}), 400
        

        # Stored hashed user password in sa variable
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create cursor to interact with database
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Users where email = %s", (email,))
        existing = cursor.fetchone()
        print(existing)

        if existing:
            return jsonify({'error': 'Email already exists'}), 409

        # Execute SQL query and commit
        cursor.execute("INSERT INTO Users (email, password) VALUES (%s, %s)", (email, hashed_password))
        db.commit()

        # Close connection
        cursor.close()

        return jsonify({'message': 'User registered successfully'})
        

    except Exception as e:
        logging.error(f"Registration failed: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/update_info', methods=['POST'])
def UpdateInfo():
    try:
            # Get data from the request
            data = request.get_json()

            # Get email and password
            email = data.get('email')
            gender = data.get('gender')
            age = data.get('age')

            # If there is no email or password entered, throw an error
            if not email:
                return jsonify({'error': 'Email and password are required'}), 400
            
            # Email validation
            if '@' not in email or '.com' not in email:
                return jsonify({'error': 'Invalid format for email'}), 400
            
            # Create cursor to interact with database
            cursor = db.cursor()
            cursor.execute("UPDATE Users SET sex = %s, age = %s WHERE email = %s", (gender, age, email))         
            db.commit()

            # Close connection
            cursor.close()

            return jsonify({'message': 'User registered successfully'})
            

    except Exception as e:
            logging.error(f"Registration failed: {str(e)}")
            return jsonify({'error': 'Registration failed'}), 500
    

# # Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    try:
        global userid
        # Get data from request
        data = request.get_json()

        # Get email and password
        email = data.get('email')
        password = data.get('password')

        # If there is no email or password entered, throw an error
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        if '@' not in email or '.com' not in email:
            return jsonify({'error': 'Invalid format for email'}), 400
        
        # Password validation
        if len(password) < 6:
            return jsonify({'error':'Password must have'}), 400
        
        # Create cursor to interact with database returning results as dictionaries
        cursor = db.cursor(dictionary=True)
        
        # Execute sql query
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))

        # Fetch the first row from the result set
        user = cursor.fetchone()

        if user:
            userid = user["uid"]
            password_from_db = user["password"]

            # Hash the user password
            hash_user = hashlib.sha256(password.encode()).hexdigest()

            if user and hash_user == password_from_db:
                return jsonify({'message': 'User logged in successfully'})
            else:
                return jsonify({'error': 'Invalid email or password'}), 401

        else:
            return jsonify({'error': 'User not found'}), 404 
          
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

# Information Endpoint
@app.route('/information', methods=['GET'])
def information():
    try:
        # Gets value of selected_date from frontend
        selected_date = request.args.get('selectedDate')
        
        # Create cursor to interact with database returning results as dictionaries
        cursor = db.cursor(dictionary=True)
        
        # Execute sql query
        cursor.execute("SELECT * FROM Food WHERE uid = %s AND DATE(timestamp) = %s", (userid, selected_date))

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Close cursor
        cursor.close()
        
        if rows:
            return jsonify(rows), 200
        else:
            return jsonify({'error': 'User not found'}), 404


    except Exception as e:
        print(f"fetch failed: {str(e)}")
        return jsonify({'error': 'fetch failed'}), 500

# Information Endpoint
@app.route('/getNutrition', methods=['POST'])
def showNutritionalInfo():
    try:
        data = request.get_json()
        
        # Get the information from the data
        food_name = data['foodName']
        portion_size = data['portion_size']

        # Call the function to get the nutrient information
        info = getNutrientInfo.getNutrientInfo(food_name, portion_size)

        #Return a 200 if successful
        return jsonify(info), 200

    except Exception as e:
        print(f"fetch failed: {str(e)}")
        return jsonify({'error': 'fetch failed'}), 500

# Run the server in debug mode - 'python flask-server.py'
if __name__ == '__main__':
    app.run(debug=True)
