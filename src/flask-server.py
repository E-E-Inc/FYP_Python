from flask import Flask, request, jsonify
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

app = Flask(__name__)
load_dotenv()

secret_key = secrets.token_hex(32) 

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

food_name = None;

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

    # takes in the global variables
    global temp_image
    global food_data
    global food_name
   
    # Gets the portion size
    data = request.get_json()
    portion_Size = data.get('portionSize')
    
    # If there is an image
    if temp_image:
        # Call the functions to process the image and get calories
        result = IdentifyFoodYolo.Identification(temp_image, portion_Size)
        calories = getCalories.Calories(result, portion_Size)

        food_name = result
        overallCalories = calories

        # Update food_data with the food name and overall calories
        food_data = {
            'result': result,
            'overall_calories': calories
        }

         # Insert data into the database
        insert_food_data(result, portion_Size, userid, overallCalories)

        # Remove the temporary file
        os.remove(temp_image)
        temp_image = None

        # Define whats in the response
        response = {
            'status': 'success',
            'message': 'Image processed successfully',
            'result': result,
            'overall_calories': calories
        }
        
        # return the response
        return jsonify(response)
        
    else:
        response = {'status': 'error', 'message': 'No image uploaded'}

    return json.dumps(response)

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

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    global userid
    try:
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

        user_id = user["uid"]
        userid = user_id

        # Extract the hashed password stored in the database for the user
        password_from_db = user["password"]

        # Hash the user password
        hash_user = hashlib.sha256(password.encode()).hexdigest()

        if user and hash_user == password_from_db:
            return jsonify({'message': 'User logged in successfully'})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

            
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

# Method to enter food into database
def insert_food_data(food_name, portion_size, uid, overallCalories):
    global userid
    try:
        cursor = db.cursor()

        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(timestamp)

         # Execute SQL query to insert data into the Food table
        cursor.execute("INSERT INTO Food (foodName, portionSize, timestamp, overallCalories, uid) VALUES (%s, %s, %s, %s, %s)",
                       (food_name, portion_size, timestamp, overallCalories, userid))

        
        # Commit changes
        db.commit()

        # Close cursor
        cursor.close()

    except Exception as e:
        logging.error(f"Failed to insert food data: {str(e)}")

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
