#import tensorflow as tf
import numpy as np
from PIL import Image
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras.applications.inception_v3 import InceptionV3

# Load the model
model = InceptionV3(weights='imagenet')

# Load and preprocess the image
img_path = 'FoodImages/Banana.jpg'
img = image.load_img(img_path, target_size=(299, 299))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Make predictions
preds = model.predict(x)

predictions = decode_predictions(preds, top=3)[0]

# Print the top predictions
for prediction in predictions:
    print(f'{prediction[1]}: {prediction[2]*100:.2f}%')