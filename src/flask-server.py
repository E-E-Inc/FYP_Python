from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from FoodRecognition import IdentifyFoodYolo

app = Flask(__name__)
CORS(app)
IMAGES_DIR = os.path.abspath(".\\src\\Images\\")

# Global variable to store the image temporarily
temp_image = None

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
    global temp_image
    data = request.get_json()
    portion_Size = data.get('portionSize')

    if temp_image:
        # Call the function to process the image
        result = IdentifyFoodYolo.Identification(temp_image, portion_Size)

        # Optionally remove the temporary file if no longer needed
        os.remove(temp_image)
        temp_image = None

        return jsonify(result=result)
    else:
        response = {'status': 'error', 'message': 'No image uploaded'}

    return json.dumps(response)

# Run the server in debug mode - 'python flask-server.py'
if __name__ == '__main__':
    app.run(debug=True)