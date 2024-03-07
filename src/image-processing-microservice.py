from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os
import mysql.connector
from werkzeug.utils import secure_filename
from FoodRecognition import IdentifyFoodYolo, getCalories, IdentifyFoodYoloManual
import mysql.connector
import secrets
import logging
import hashlib
from dotenv import load_dotenv
from datetime import datetime
import requests

app = Flask(__name__)
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

app.config['IMAGES_DIR'] = IMAGES_DIR

# Handle POST request to '/upload' endpoint for uploading an image
@app.route('/upload', methods=['POST'])
def upload():

    # if there is no file part
    if 'file' not in request.files:
        return jsonify({'error':'no file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)      
        # Save the file to a temporary location to be processed
        temp_path = os.path.join(IMAGES_DIR, filename)
        file.save(temp_path)
        print("File upload successful")
        return jsonify({'message': 'File uploaded successfully', 'file_path': temp_path})
    else: 
        return jsonify({'error': 'Invalid file format'})

@app.route('/process', methods=['POST'])
def process():
    print("Here girlie")
    try:
        print("In /process microservice")
       
        # Gets the portion size
        data = request.get_json()
        filePath = data.get('filePath')
        portion_Size = data.get('portionSize')
        uid = data.get('uid')

        print("Session uid in /process: ", uid)

        print(data)
        if not filePath:
            return jsonify({'error': 'No file path provided'}), 400

        if not portion_Size:
            return jsonify({'error': 'No portion size provided'}), 400

        # Call the functions to process the image and get calories
        result = IdentifyFoodYolo.Identification(filePath, portion_Size)
        calories = getCalories.Calories(result, portion_Size)
        print(result)
        print(calories)
        # Insert data into the database
        insert_food_data(result, portion_Size, calories, uid)
        return jsonify({
                'status': 'success',
                'result': result,
                'calories': calories
            })
    
    except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
@app.route('/process_manually', methods=['POST'])
def process_manually():
    try:
        print("In /process_manually microservice")
       
        # Gets the portion size
        data = request.get_json()
        
        food_Name = data.get('foodName')
        portion_Size = data.get('portion')
        uid = data.get('uid')

        print("Session uid in /process: ", uid)
        print("Name", food_Name)
        print ("Portion", portion_Size)

        if not portion_Size:
            return jsonify({'error': 'No portion size provided'}), 400

        # Call the functions to get calories
        calories = getCalories.Calories(food_Name, portion_Size)
        print(calories)
        print("im here girlie")
        # Insert data into the database
        insert_food_data(food_Name, portion_Size, calories, uid)
        return jsonify({
                'status': 'success',
                'result': food_Name,
                'calories': calories
            })
    
    except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
# Method to enter food into database
def insert_food_data(food_name, portion_size, overallCalories, uid):
    print("HERE!!!!!")
    try:
        print("User id>",uid)
        print(food_name)
        print(portion_size)
        print(overallCalories)

        if uid:
            print("Here girlies")
            cursor = db.cursor()

            # Get current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(timestamp)
            print("Almost there girlie")
            # Execute SQL query to insert data into the Food table
            cursor.execute("INSERT INTO Food (foodName, portionSize, timestamp, overallCalories, uid) VALUES (%s, %s, %s, %s, %s)",
                        (food_name, portion_size, timestamp, overallCalories, uid))

            
            # Commit changes
            db.commit()

            # Close cursor
            cursor.close()
            
            return jsonify({'Success': 'Inserted'})

        else:
            return jsonify({'error': 'failed'})

    except Exception as e:
        logging.error(f"Failed to insert food data: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True, port=5001)