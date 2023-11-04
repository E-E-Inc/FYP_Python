import argparse
from ultralytics import YOLO
import cv2

def Identification(image_path):
    #define model
    model = YOLO('yolov8n.pt')

    # Read image and store it 
    load_image = cv2.imread(image_path)

    # Run the model on the image and store the results
    result = model(load_image)

    #Store the class id of the first detected object 
    detected_class_id = result[0].pred[0]

    #List of Ultralytics classes
    ultralytics_classes = {
      20: 'banana', 21: 'apple', 22: 'sandwich', 23: 'orange', 24: 'broccoli', 25: 'carrot', 26: 'hot dog',
        27: 'pizza', 28: 'donut', 29: 'cake'

    }

    #If the item name is in the class
    if(detected_class_id in ultralytics_classes):
        #stores the name of the coresponding class from ultralytics_classes
        detected_item = ultralytics_classes[detected_class_id]
    else:
        detected_item='Unknown'

    print(f"Item detected is {detected_item}")
    s = detected_item
    return s

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an image.')
    parser.add_argument('image_path', type=str, help='The path to the image file')

    args = parser.parse_args()

    Identification(args.image_path)