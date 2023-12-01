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
    
    #List of classes
    dataset_classes = {
0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck',
 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
   14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
     22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie',
       28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite',
         34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard',
           38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork',
             43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
               49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 
               54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 
               59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 
               64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone',
                 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator',
                   73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush', 80: 'alcohol', 81: 'alcohol_glass', 82: 'almond', 83: 'avocado', 84: 'blackberry', 85: 'blueberry', 86: 'bread', 87: 'bread_loaf', 88: 'capsicum', 89: 'cheese', 90: 'chocolate', 91: 'cooked_meat', 92: 'dates', 93: 'egg', 94: 'eggplant', 95: 'ice cream', 96: 'milk', 97: 'milk_based_beverage', 98: 'mushroom', 99: 'non_milk_based_beverage', 100: 'pasta', 101: 'pineapple', 102: 'pistachio', 103: 'pizza', 104: 'raw_meat', 105: 'roti', 106: 'spinach', 107: 'strawberry', 108: 'tomato', 109: 'whole_egg_boiled'
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