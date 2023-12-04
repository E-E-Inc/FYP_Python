import argparse
from ultralytics import YOLO
import cv2

def Identification(image_path):
    #define model
    model = YOLO('runs//detect//tester5//weights//best.pt')

    # Read image and store it 
    load_image = cv2.imread(image_path)

    # Run the model on the image and store the results
    result = model(load_image)

   # List of classes
   dataset_classes = {
       1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
       6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
       11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
       16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep',
       21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe',
       27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase',
       34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite',
       39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard', 42: 'surfboard',
       43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork',
       49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple',
       54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog',
       59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch',
       64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv',
       73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell phone',
       78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator',
       84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear',
       89: 'hair drier', 90: 'toothbrush', 91: 'alcohol', 92: 'alcohol_glass',
       93: 'almond', 94: 'avocado', 95: 'blackberry', 96: 'blueberry', 97: 'bread',
       98: 'bread_loaf', 99: 'capsicum', 100: 'cheese', 101: 'chocolate',
       102: 'cooked_meat', 103: 'dates', 104: 'egg', 105: 'eggplant', 106: 'ice cream',
       107: 'milk', 108: 'milk_based_beverage', 109: 'mushroom', 110: 'non_milk_based_beverage',
       111: 'pasta', 112: 'pineapple', 113: 'pistachio', 114: 'pizza', 115: 'raw_meat',
       116: 'roti', 117: 'spinach', 118: 'strawberry', 119: 'tomato', 120: 'whole_egg_boiled'
   }

    #checks if there are detection results and else, it prints no item detected
    if result:
        #Loops through each detected bounding box in the first result
        for box in result[0].boxes:
            #Retrieves class id for the detected object
            detected_class_id = box.cls.item()
            #Maps the class id to the class name
            #if it is not found then its unknown
            detected_item = dataset_classes.get(detected_class_id, 'Unknown')
            print(f"Item detected is {detected_class_id}")
            print(f"{detected_item}")
    else:
        print("No items detected.")

    s = detected_item
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