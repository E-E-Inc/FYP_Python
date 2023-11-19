from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model.train(
    data = 'src\Dataset\data.yaml',
    imgsz = 640,
    epochs=10,
    batch=8,
    name = 'Custom_dataset'
)