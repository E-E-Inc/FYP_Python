import argparse
from ultralytics import YOLO
import cv2


model = YOLO('runs//detect//refined_dataset//weights//last.pt')

class_names = model.names

print("Classes in the model:")
\
for i, class_name in enumerate(class_names):
    print(f"{i + 1}. {class_name}")