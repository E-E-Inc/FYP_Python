from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import mysql.connector
from werkzeug.utils import secure_filename
from FoodRecognition import IdentifyFoodYolo, getCalories
import mysql.connector
import logging
import os

# from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
CORS(app)

IMAGES_DIR = os.path.abspath(".\\src\\Images\\")

app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'  # session type

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

# MySQL Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")), 
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

# Handle POST request to '/process' endpoint for processing an image
@app.route('/process', methods=['POST'])
def process():
    try:
        # Gets the portion size
        data = request.get_json()
        filePath = data.get('filePath')
        portion_Size = data.get('portionSize')
        uid = data.get('uid')

        if not filePath:
            return jsonify({'error': 'No file path provided'}), 400

        if not portion_Size:
            return jsonify({'error': 'No portion size provided'}), 400

        # Call the functions to process the image and get calories
        result = IdentifyFoodYolo.Identification(filePath, portion_Size)
        calories = getCalories.Calories(result, portion_Size)
       
        # Insert data into the database
        insert_food_data(result, portion_Size, calories, uid)
        return jsonify({
                'status': 'success',
                'result': result,
                'calories': calories
            })
    
    except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
# Handle POST request to '/process_manually' endpoint for processing an image manually
@app.route('/process_manually', methods=['POST'])
def process_manually():
    try:       
        # Gets the portion size
        data = request.get_json()
        print(data)

        food_Name = data.get('foodName')
        portion_Size = data.get('portion')

        uid = data.get('uid')
        print("uid in /process_manually: ", uid)

        if not portion_Size:
            return jsonify({'error': 'No portion size provided'}), 400

        # Call the functions to get calories
        calories = getCalories.Calories(food_Name, portion_Size)
      
        # Insert data into the database
        insert_food_data(food_Name, portion_Size, calories, uid)
        return jsonify({
                'status': 'success',
                'result': food_Name,
                'calories': calories
            })
    
    except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
# Method to entering food into database
def insert_food_data(food_name, portion_size, overallCalories, uid):
    print("in Insert food data")
    try:
        if uid:
            cursor = db.cursor()
            print("User ID in insert_food_data: ", uid)
            # Get current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            # Execute SQL query to insert data into the Food table
            cursor.execute("INSERT INTO Food (foodName, portionSize, timestamp, overallCalories, uid) VALUES (%s, %s, %s, %s, %s)",
                        (food_name, portion_size, timestamp, overallCalories, uid))
            print("Inserted")
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))


    # "processing failed: HTTPSConnectionPool(host='fyppython-production.up.railway.appprocess_manually', port=443): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPSConnection object at 0x7f0a20ab33d0>: Failed to resolve 'fyppython-production.up.railway.appprocess_manually' ([Errno -2] Name or service not known)\"))"
