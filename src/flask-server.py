from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from FoodRecognition import IdentifyFoodYolo

app = Flask(__name__)
CORS(app)

# Handle POST request to '/upload' endpoint for uploading an image
@app.route('/upload', methods=['POST'])
def upload():
    # Get the file from post request
    file = request.files['file']
    # file_contents = file.read()
    

    # TODO: Process the image asynchronously using a message queue
    # For now just call the function directly
    if file:
        # Secure the filename to avoid unsafe characters
        filename = secure_filename(file.filename)
        # Save the file to a temporary location to be processed
        temp_path = os.path.join('/path/to/temp', filename)
        file.save(temp_path)

        # Call the function to process the image
        result = IdentifyFoodYolo.Identification(temp_path)

        # Optionally remove the temporary file if no longer needed
        os.remove(temp_path)
        
        return jsonify(result=result)

    # Return the result
    # if file_contents is None:
    if file.filename == '':
        response = {'status': 'error', 'message': 'Error processing image'}
    else:
        response = {'status': 'success', 'message': 'File uploaded successfully'}

    return json.dumps(response)

# Run the server in debug mode - 'python flask-server.py'
if __name__ == '__main__':
    app.run(debug=True)