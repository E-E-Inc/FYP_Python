from flask import Flask, request, jsonify, session, redirect, url_for
#from functools import wraps
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from FoodRecognition import getNutrientInfo
from CalculateBMR import BMR
import mysql.connector  
#import secrets
import logging
import hashlib
from dotenv import load_dotenv
from datetime import datetime
import requests
from flask_cors import CORS
from flask import g

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'  # session type

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

MICROSERVICE_URL = 'http://localhost:5001'  

CORS(app, supports_credentials=True)
IMAGES_DIR = os.path.abspath(".\\src\\Images\\")

# MySQL Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"), 
    user=os.getenv("DB_USER"),  
    password=os.getenv("DB_PASSWORD"), 
    database=os.getenv("DB_NAME")
)

# Global variables
temp_image = None
bmr = None
food_data = None

@app.before_request
def before_request():
    g.db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"), 
    user=os.getenv("DB_USER"),  
    password=os.getenv("DB_PASSWORD"), 
    database=os.getenv("DB_NAME")
)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Handle POST request to '/image_upload' endpoint for uploading an image
@app.route('/image_upload', methods=['POST'])
def image_upload():

    # Get the file from post request
    file = request.files['file']

    if not file:
        return jsonify({'error':'no file part'})
    
    try:
        url= f'{MICROSERVICE_URL}/upload'
        files = {'file': file}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'upload failed'})

    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'})

# Handle POST request to '/image_process' endpoint for processing an image
@app.route('/image_process', methods=['POST'])
def image_process():
    uid = session.get('uid')
    # Gets the portion size
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'})
    
    print("Session uid in /information: ", uid)
    # Add the user ID to the data
    data['uid'] = uid
    print("Data: ", data)

    try:
        url= f'{MICROSERVICE_URL}/process'
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'processing failed'})
    
    except Exception as e:
        return jsonify({'error': f'processing failed: {str(e)}'})
   
# Handle POST request to '/image_process_manually' endpoint for processing an image manually
@app.route('/image_process_manually', methods=['POST'])
def image_process_manually():

    #global userid
    uid = session.get('uid')
    print("Session uid in /image_process_manually: ", uid)
    # Gets the portion size
    data = request.get_json()

    # Extract food name and portion size from the JSON data
    food_name = data.get('foodName')
    portion_size = data.get('portion')
    
    if not data:
        return jsonify({'error': 'No data provided'})
    
    # Add the user ID to the data
    data['uid'] = uid
    print("Food Name", food_name)
    print("Portion Size", portion_size)
    try:
        url= f'{MICROSERVICE_URL}/process_manually'
        payload = {
            'foodName': food_name,
            'portion': portion_size,
            'uid': uid
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'processing failed'})
    
    except Exception as e:
        return jsonify({'error': f'processing failed: {str(e)}'})
   
# Handle POST request to '/register' endpoint for registering a user
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

# Handle POST request to '/update_info' endpoint for adding additional user info
@app.route('/update_info', methods=['POST'])
def UpdateInfo():
    global bmr
    try:
            # Get data from the request
            data = request.get_json()

            # Get email and password
            email = data.get('email')
            gender = data.get('gender')
            age = data.get('age')
            height = data.get('height')
            weight = data.get('weight')

            # If there is no email or password entered, throw an error
            if not email:
                return jsonify({'error': 'Email and password are required'}), 400
            
            # Email validation
            if '@' not in email or '.com' not in email:
                return jsonify({'error': 'Invalid format for email'}), 400
            
             # Validate gender
            gender = data.get('gender')
            if gender not in ['male', 'female']:
                return jsonify({'error': 'Invalid gender'}), 400

            # Validate age
            age = data.get('age')
            if not age or not 0 < int(age) < 100:
                return jsonify({'error': 'Invalid age'}), 400

            # Validate height
            height = data.get('height')
            if not height or len(height) > 3 or not height.isdigit():
                return jsonify({'error': 'Invalid height'}), 400

            # Validate weight
            weight = data.get('weight')
            if not weight or len(weight) > 3 or not weight.isdigit():
                return jsonify({'error': 'Invalid weight'}), 400
            
            total = BMR(gender, age, height, weight)
            bmr = total
            # Create cursor to interact with database
            cursor = db.cursor()
          
            cursor.execute("UPDATE Users SET sex = %s, age = %s, weight= %s, height= %s, NeededCalories=%s WHERE email = %s", (gender, age, weight, height, total, email))         
            db.commit()

            
            # Close connection
            cursor.close()
            return jsonify({'message': 'User registered successfully', 'total': total})

    except Exception as e:
            logging.error(f"Registration failed: {str(e)}")
            return jsonify({'error': 'Registration failed'}), 500

@app.route('/')
def home():
    if 'uid' in session:
        return f"Welcome back, user {session['uid']}!"
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    # Clear server-side session or token here if any
    session.pop('uid', None)
    print('Logged out')
    # Then return a success response
    return {"status": "success"}, 200

# Handle POST request to '/login' endpoint for logging in a user
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get data from request
        data = request.get_json()
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
        print("User: ", user)
        if user:
            password_from_db = user["password"]
        
            # Hash the user password
            hash_user = hashlib.sha256(password.encode()).hexdigest()
 
            if user and hash_user == password_from_db:

                session['uid'] = user["uid"]

                print("Session: ", session['uid'])
                print("User logged in successfully")

                response = jsonify({'message': 'Logged in', 'uid': str(session['uid'])})

                response.headers['Set-Cookie'] = 'session uid =' + str(session['uid'])
                return response
                
            else:
                return jsonify({'error': 'Invalid email or password'}), 401

        else:
            return jsonify({'error': 'User not found'}), 404 
          
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

# Handle GET request to '/information' endpoint for getting user information and food for a particular day
@app.route('/information', methods=['GET'])
def information():
    try:
        # print("Session: ", session)
        sessionuid = session.get('uid')
        print("Session uid in /information: ", sessionuid)

        if sessionuid is None:
            return jsonify({'error': 'Not logged in'}), 401

        # Gets value of selected_date from frontend
        selected_date = request.args.get('selectedDate')
        
        # Create cursor to interact with database returning results as dictionaries
        cursor = g.db.cursor(dictionary=True)
        # print("Session uid in /information: ",sessionuid)

        #Execute sql query
        cursor.execute("SELECT * FROM Food WHERE uid = %s AND DATE(timestamp) = %s", (sessionuid, selected_date))

        # Fetch all rows from the result set
        rows = cursor.fetchall()
        # print("Rows: ", rows)
        # Close cursor
        cursor.close()
        
        if rows:
            return jsonify(rows), 200
        else:
            return jsonify({'error': 'User not found'}), 404


    except Exception as e:
        print(f"fetch failed: {str(e)}")
        return jsonify({'error': 'fetch failed'}), 500

@app.route('/needed_calories', methods=['GET'])
def get_needed_calories():
    try:
        
        uidcals = session.get('uid')
        print("Session uid in /needed_calories: ", session.get('uid'))
        if not uidcals:
            return jsonify({'error': 'Missing uid'}), 400

        # Create a cursor to interact with the database
        cursor = db.cursor(dictionary=True)

        # Execute a SQL query to get the NeededCalories for the user with the given uid
        cursor.execute("SELECT NeededCalories FROM Users WHERE uid = %s", (uidcals,))

        # Fetch the first row from the result set
        row = cursor.fetchone()
        print("Row: ", row)
        # Close the cursor
        cursor.close()

        if row:
            # If a row was found, return the NeededCalories
            return jsonify(row["NeededCalories"]), 200
        else:
            # If no row was found, return an error
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(f"fetch failed: {str(e)}")
        return jsonify({'error': 'fetch failed'}), 500
    
# Handle POST request to '/getNutrition' endpoint for getting food nutritional information
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
    app.run(debug=True, port=5000)