import argparse
from ultralytics import YOLO
import cv2

def Identification(image_path):
    model = YOLO('runs//detect//Custom_dataset//weights//best.pt')

    # Read image and store it 
    load_image = cv2.imread(image_path)

    detected_item = 'Unknown'

    # Run the model on the image and store the results
    result = model(load_image)
    
    if result and result[0].boxes.cls.nelement() > 0:
        detected_class_id = result[0].boxes.cls.item()

        #List of classes
        dataset_classes = {
        0: 'alcohol', 1: 'alcohol_glass', 2: 'almond', 3: 'avocado', 4: 'blackberry',
        5: 'blueberry', 6: 'bread', 7: 'bread_loaf', 8: 'capsicum', 9: 'cheese',
        10: 'chocolate', 11: 'cooked_meat', 12: 'dates', 13: 'egg', 14: 'eggplant',
        15: 'icecream', 16: 'milk', 17: 'milk_based_beverage', 18: 'mushroom',
        19: 'non_milk_based_beverage', 20: 'pasta', 21: 'pineapple', 22: 'pistachio',
        23: 'pizza', 24: 'raw_meat', 25: 'roti', 26: 'spinach', 27: 'strawberry',
        28: 'tomato', 29: 'whole_egg_boiled'
        }

        if(detected_class_id in dataset_classes):
            detected_item= dataset_classes[detected_class_id]
            
        print(f"Item detected is {detected_item}")

     
    else:
        detected_class_id = None

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