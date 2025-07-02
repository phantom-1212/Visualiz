# Visualiz
AI Vision Assistant for the Visually Impaired. It uses Streamlit, which is an easier way to run a Python code for the implementation of Web apps without using full stack.

# 🧠 Visualz — AI Vision Assistant for the Visually Impaired

Visualz is an intelligent web-based assistant designed to empower visually impaired individuals. It uses real-time object detection, OCR (Optical Character Recognition), and speech synthesis to describe the world around the user — either from an uploaded image or a live webcam feed.

## 🌟 Features

- 📷 **Upload Image** or use 📹 **Live Webcam**
- 🎯 Real-time object detection using **YOLOv5**
- 🧾 Text extraction from images using **OCR (Tesseract)**
- 🔊 Voice feedback using **Text-to-Speech (pyttsx3)**
- 🖼️ Stylish UI with gradient backgrounds and logo branding
- 🧠 Smart summarization: avoids repeating the same voice output
- 🧪 Optimized for performance using `torch` and `ultralytics`

## 🚀 How It Works

1. **Upload an image** OR **start your webcam**.
2. The app detects objects using YOLOv5.
3. It also extracts any visible text (OCR).
4. Detected labels and text are **spoken aloud** via TTS.
5. In webcam mode, the app continuously describes updated scenes.

## 🛠️ Tech Stack

| Tool/Library      | Purpose                     |
|-------------------|-----------------------------|
| `Streamlit`       | Web frontend                |
| `YOLOv5 (Ultralytics)` | Object detection        |
| `OpenCV`          | Webcam & image handling     |
| `pytesseract`     | OCR (text reading)          |
| `pyttsx3`         | Text-to-speech synthesis    |
| `Pillow (PIL)`    | Image processing            |

---

## 📂 Folder Structure

📁 Vision-Assistant/
├── app.py # Main Streamlit application
├── detect.py # Object detection functions
├── ocr.py # OCR processing
├── tts.py # Text-to-speech functions
├── vision_utils.py # Helper functions
├── logo.png # Top-left corner branding image
├── requirements.txt # Python dependencies
└── README.md # You're reading it!


---

## ⚙️ Installation & Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/vision-assistant.git
cd vision-assistant
pip install -r requirements.txt

If you're missing Tesseract:

    Windows: Install from https://github.com/tesseract-ocr/tesseract

    Set the path in ocr.py if needed.

3️⃣ Run the app

streamlit run app.py
