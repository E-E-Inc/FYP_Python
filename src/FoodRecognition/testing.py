from ultralytics import YOLO
import cv2

#define model
#model = YOLO('runs\\detect\\Custom_dataset\\weights\\best.pt')
model = YOLO('yolov8n.pt')

#define image
#image = 'src\\Dataset\\train\\images\\00000001_jpg.rf.0174e356d577b61b2f277dfbf3ca1ffc.jpg'
image = 'src\\Images\\Banana.jpg'

# Read image and store it 
load_image = cv2.imread(image)

# Run the model on the image and store the results
result = model(image)

#Store the class id of the first detected object 
detected_class_id = result[0].boxes.cls.item()

 # List of classes
dataset_classes = {
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
if(detected_class_id):
    #stores the name of the coresponding class from ultralytics_classes
    detected_item = dataset_classes[detected_class_id]
else:
    detected_item='Unknown'

#print(f"Item detected is {detected_class_id}")
s = detected_item