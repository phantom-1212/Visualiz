from ultralytics import YOLO

def detect_objects(image, model):
    """
    Detect objects in a PIL or NumPy image using the given YOLO model.
    Returns a list of detected class labels.
    """
    results = model(image)
    labels = [result.names[int(cls)] for result in results for cls in result.boxes.cls]
    return labels

def detect_objects_from_array(frame, model):
    """
    Detect objects in an OpenCV frame using the given YOLO model.
    Returns the list of labels and the annotated frame.
    """
    results = model(frame)
    labels = [result.names[int(cls)] for result in results for cls in result.boxes.cls]
    annotated_frame = results[0].plot()
    return labels, annotated_frame
