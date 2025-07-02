import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import torch
import base64

# Assuming these modules are available in the environment
# If they are custom, ensure they are in the same directory or accessible.
try:
    from detect import detect_objects, detect_objects_from_array
    from ocr import read_text_from_image
    from vision_utils import load_image, summarize_labels
    from tts import speak_text
except ImportError as e:
    st.error(f"Error importing custom modules: {e}. Please ensure detect.py, ocr.py, vision_utils.py, and tts.py are in the same directory.")
    st.stop() # Stop execution if essential modules are missing

from ultralytics import YOLO

# Load YOLO model only once to avoid re-loading on rerun
@st.cache_resource
def load_yolo_model():
    return YOLO("yolov5s.pt")

model = load_yolo_model()

st.set_page_config(page_title="AI Vision Assistant", layout="centered")

# --- Custom CSS for background, header, and buttons ---
st.markdown("""
    <style>
    /* Gradient Background */
    html, body, .main, .stApp {
        background: linear-gradient(to right, #fceabb, #f8b500);
        background-attachment: fixed;
    }

    /* Adjust Streamlit's main block to ensure content starts higher and remove default header */
    .stApp > header {
        display: none; /* Hide default Streamlit header */
    }
    /* Target specific Streamlit div for main content padding */
    .st-emotion-cache-z5fcl4, .st-emotion-cache-1gh0r7o, .st-emotion-cache-uf99v8 { 
        padding-top: 0rem;
        padding-left: 1rem; /* Adjust general left/right padding if needed */
        padding-right: 1rem;
    }

    /* Custom Header Container for Logo and Title */
    .custom-header {
        display: flex;
        align-items: center; /* Vertically center elements within the flex container */
        justify-content: center; /* Horizontally center the title */
        width: 100%;
        position: relative; /* Essential for absolute positioning of the logo */
        padding-top: 20px; /* Overall padding at the top of the header area */
        padding-bottom: 20px;
    }

    /* Logo Positioning */
    .logo-container {
        position: absolute; /* Position the logo independently */
        top: -23px;  /* <<< ADJUST THIS VALUE TO MOVE LOGO UP/DOWN */
        left: -456px; /* <<< ADJUST THIS VALUE TO MOVE LOGO LEFT/RIGHT */
        z-index: 1000; /* Ensure it's on top of other elements */
    }
    .logo-container img {
        height: 78px; /* Adjust logo height as needed */
        width: 105px;
        border-radius: 10%; /* Optional: round corners for the logo */
    }

    /* Main Title Styling */
    .main-title {
        text-align: center; /* Center the text itself */
        font-size: 67px;
        font-weight: bold;
        color: white;
        margin: 0; /* Remove default margin from h1 */
        flex-grow: 1; /* Allow title div to take up available space and push to center */
    }

    /* Subtitle Styling */
    .subtitle {
        text-align: center;
        font-size: 36px;
        color: white;
        margin-top: 0px; /* Ensure no extra space above it */
        margin-bottom: 30px;
    }

    /* ALL BUTTONS TO ORANGE */
    .stButton > button,
    .stFileUploader > div > button { /* Target both regular buttons and file uploader button */
        background-color: #FFA500; /* Orange */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold; /* Make button text bold */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2); /* Subtle shadow for depth */
    }
    .stButton > button:hover,
    .stFileUploader > div > button:hover {
        background-color: #FF8C00; /* Darker Orange on hover */
        box-shadow: 3px 3px 7px rgba(0,0,0,0.3); /* Slightly larger shadow on hover */
    }

    /* Checkbox label color */
    .stCheckbox > label > div > span {
        color: white; /* Color for checkbox label */
            font-size: 45px;
    }
    /* Ensure other text is visible against background */
    .st-emotion-cache-10q7q25 p, .st-emotion-cache-10q7q25 h3, .st-emotion-cache-10q7q25 label {
        color: white; /* Adjust color for paragraph, subheaders, and labels */
    }
    .st-emotion-cache-10q7q25 .stAlert { /* Adjust alert colors for better visibility */
        background-color: rgba(255, 255, 255, 0.2); /* Semi-transparent white */
        color: #333; /* Darker text for contrast on lighter alert background */
    }
    </style>
""", unsafe_allow_html=True)

# Function to convert image to base64
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return encoded
    except FileNotFoundError:
        st.error(f"Error: Logo file '{image_path}' not found. Please ensure it's in the correct directory.")
        return None

logo_filename = "visualiz_logo.png"  # Renamed from image_c0e0b8.png for clarity
encoded_image = image_to_base64(logo_filename)

# --- Header Section with Logo and Centered Title ---
# The custom-header div contains both the logo (absolutely positioned)
# and the centered title (flex-grown).
if encoded_image:
    st.markdown(f"""
        <div class="custom-header">
            <div class="logo-container">
                <img src="data:image/png;base64,{encoded_image}" alt="App Logo">
            </div>
            <div class="main-title">
                AI Vision Assistant for the Visually Impaired
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # Fallback if logo not found, just display the title centered
    st.markdown('<div class="main-title">AI Vision Assistant for the Visually Impaired</div>', unsafe_allow_html=True)


# Subtitle
st.markdown('<div class="subtitle">Upload an image or start real-time detection using your webcam.</div>', unsafe_allow_html=True)

# -------------------------
# 📷 IMAGE UPLOAD SECTION
# -------------------------
uploaded_img = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
use_ocr = st.checkbox("🔤 Also read text from image (OCR)", value=True)

if uploaded_img:
    image = load_image(uploaded_img)
    if image is not None:
        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("🔍 Detecting objects..."):
            labels = detect_objects(image, model)
        label_summary = summarize_labels(labels)

        if label_summary:
            st.success(f"🧠 Detected: {label_summary}")
            speak_text(label_summary)
        else:
            st.info("No prominent objects detected.")

        if use_ocr:
            with st.spinner("🧾 Extracting text..."):
                text = read_text_from_image(image)
            if text:
                st.success(f"📖 Text: {text}")
                speak_text("The text says: " + text)
            else:
                st.info("No discernible text found.")

# -------------------------
# 🎥 WEBCAM DETECTION SECTION
# -------------------------
st.markdown("---")
st.subheader("🎥 Real-Time Object Detection via Webcam")

# Use st.session_state to manage webcam state more robustly
if 'webcam_active' not in st.session_state:
    st.session_state.webcam_active = False

col1, col2 = st.columns(2)
with col1:
    start_button = st.button("Start Webcam Detection", key="start_webcam_btn")
with col2:
    stop_button = st.button("Stop Webcam Detection", key="stop_webcam_btn")

if start_button:
    st.session_state.webcam_active = True
    st.warning("Click the STOP button or close the tab to end detection.")
    st.caption("💡 Ensure your browser tab is unmuted to hear audio.")

if stop_button:
    st.session_state.webcam_active = False
    st.info("Webcam detection stopped.")

if st.session_state.webcam_active:
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    last_spoken = ""
    # Store initial time to limit speaking frequency, if desired
    # last_speech_time = time.time()

    if not cap.isOpened():
        st.error("❌ Could not access webcam. Please ensure it's not in use by another application.")
        st.session_state.webcam_active = False # Reset state
    else:
        while st.session_state.webcam_active and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("⚠️ Failed to read frame from webcam.")
                st.session_state.webcam_active = False
                break

            # Resize frame to optimize processing, common for YOLO input
            frame_resized = cv2.resize(frame, (640, 480))

            # Perform detection
            labels, annotated_frame = detect_objects_from_array(frame_resized, model)

            # Convert BGR to RGB for Streamlit display
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            stframe.image(rgb_frame, channels="RGB", use_container_width=True)

            if labels:
                summary = summarize_labels(labels)
                # Only speak if the summary has changed to avoid repetition
                if summary != last_spoken:
                    speak_text(summary)
                    last_spoken = summary
            # else:
            #     # Optionally speak "No objects detected" if nothing is found and last_spoken was not empty
            #     if last_spoken != "No objects detected.":
            #         speak_text("No objects detected.")
            #         last_spoken = "No objects detected."

            # Small delay to prevent overwhelming the CPU and ensure smooth display
            time.sleep(0.05)

        cap.release()
        cv2.destroyAllWindows() # Ensures any CV2 windows are closed if opened
        if st.session_state.webcam_active: # If loop exited by condition other than stop button click
             st.info("Webcam detection ended.")
        st.session_state.webcam_active = False # Ensure state is reset