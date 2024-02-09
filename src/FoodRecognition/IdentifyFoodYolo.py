import argparse
from ultralytics import YOLO
import cv2
from FoodRecognition import getCalories
def Identification(image_path, portion_size):
    #define model
    model = YOLO('yolov8n.pt')

    # Read image and store it 
    load_image = cv2.imread(image_path)

    # Run the model on the image and store the results
    result = model(load_image, classes=[46, 47, 48, 49, 50, 51, 52, 53, 54])
    
    if result and result[0].boxes.cls.nelement() > 0:
        detected_class_id = result[0].boxes.cls.item()
    else:
        detected_class_id = None

    #List of Ultralytics classes
    ultralytics_classes = {
        0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
        7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter',
        13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant',
        21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie',
        28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite',
        34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
        39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
        46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog',
        53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
        60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
        67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator',
        73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier',
        79: 'toothbrush'
    }

    #If the item name is in the class
    if(detected_class_id in ultralytics_classes):
        #stores the name of the coresponding class from ultralytics_classes
        detected_item = ultralytics_classes[detected_class_id]
    else:
        detected_item='Unknown'

    print(f"Item detected is {detected_item}")
    s = detected_item

    # Call the calories function 
    getCalories.Calories(s, portion_size)

    # Reset the detected item
    #detected_class_id = None
    return s

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
