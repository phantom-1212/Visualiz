# ocr.py
import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'])

def read_text_from_image(image):
    image_np = np.array(image)
    results = reader.readtext(image_np)
    extracted_text = " ".join([res[1] for res in results])
    return extracted_text
