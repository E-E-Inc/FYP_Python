import argparse
from ultralytics import YOLO
import cv2

def Identification(image_path):
    model = YOLO('runs//detect//refined_dataset//weights//best.pt')

    # Read image and store it 
    load_image = cv2.imread(image_path)

    detected_item = 'Unknown'

    # Run the model on the image and store the results
    result = model(load_image)
    
    if result and result[0].boxes.cls.nelement() > 0:
        detected_class_id = result[0].boxes.cls.item()
        print(f"Class ID detected is {detected_class_id}")

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