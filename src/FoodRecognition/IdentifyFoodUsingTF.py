import argparse
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications.vgg19 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

def Identification(image_path):
    model = VGG19(weights='imagenet')

    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)

    predictions = decode_predictions(preds, top=1)[0]
    detected_item = predictions[0][1]
    print(f"Item detected is {detected_item}")
    return detected_item

#Checks if script is being run directly
if __name__ == '__main__':
    #Sets up command line argument parser for the script and provide a description 
    parser = argparse.ArgumentParser(description='Process an image.')

    #Specifies that image_path must be a string
    parser.add_argument('image_path', type=str, help='The path to the image file')

    #Parses the arguement when the script is run
    args = parser.parse_args()
    
    #Calls Identification function with the argument image_path
    Identification(args.image_path)