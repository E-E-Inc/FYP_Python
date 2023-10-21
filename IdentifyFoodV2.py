from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the FoodAI model
model = MobileNetV2(weights='imagenet')

# Load and preprocess the food image
img_path = 'FoodImages/Banana.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Make predictions
preds = model.predict(x)

# Decode predictions
predictions = decode_predictions(preds, top=3)[0]

# Print the top predictions
for prediction in predictions:
    print(f'{prediction[1]}: {prediction[2]*100:.2f}%')
