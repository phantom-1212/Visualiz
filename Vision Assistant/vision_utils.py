# utils.py

from PIL import Image
import numpy as np
import io

def load_image(uploaded_file):
    """
    Convert uploaded file to PIL Image.
    """
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def image_to_numpy(image):
    """
    Convert PIL Image to numpy array.
    """
    return np.array(image)

def summarize_labels(labels):
    """
    Converts a list of object labels into a natural sentence.
    """
    if not labels:
        return "No objects detected."
    
    unique_labels = list(set(labels))
    if len(unique_labels) == 1:
        return f"I see a {unique_labels[0]}."
    else:
        return "I see: " + ", ".join(unique_labels[:-1]) + " and " + unique_labels[-1] + "."

def combine_text_and_labels(text, labels):
    """
    Combines OCR text and object detection results into a single readable summary.
    """
    label_summary = summarize_labels(labels)
    if text:
        return f"{label_summary}. Also, the text says: {text}"
    else:
        return label_summary
