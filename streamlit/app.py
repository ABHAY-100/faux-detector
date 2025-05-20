import os
import cv2
import numpy as np
import tempfile
import requests
from tqdm import tqdm
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Constants
MODEL_URL = 'https://faux-cnn-model.s3.eu-north-1.amazonaws.com/cnn_model.h5'
INPUT_SIZE = (128, 128)
ALLOWED_EXTENSIONS = ('.mp4', '.avi', '.mov', '.jpg', '.jpeg', '.png')

@st.cache_resource
def load_model_from_s3():
    """Load model from public S3."""
    temp_model_path = 'temp_model.h5'
    if not os.path.exists(temp_model_path):
        st.write("🔄 Downloading model from S3...")
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))

        with open(temp_model_path, 'wb') as f:
            with st.spinner("Downloading model..."):
                for data in tqdm(response.iter_content(chunk_size=8192), total=total_size//8192):
                    f.write(data)
    return load_model(temp_model_path)

def preprocess_frame(frame):
    return img_to_array(cv2.resize(frame, INPUT_SIZE)) / 255.0

def predict_batch(model, frames, batch_size=32):
    preprocessed = np.array([preprocess_frame(frame) for frame in frames])
    return model.predict(preprocessed, batch_size=batch_size, verbose=0)

def classify_video(video_path, model, num_frames=20):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open video")

    frames = []
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, frame_count // num_frames)

    for i in range(0, frame_count, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret and len(frames) < num_frames:
            frames.append(frame)

    cap.release()
    predictions = predict_batch(model, frames)
    return predictions.flatten().tolist()

# Load model
model = load_model_from_s3()

# Streamlit UI
st.title("Deepfake Detector AI")
st.write("Upload an image or video file to detect if it's a deepfake.")

uploaded_file = st.file_uploader("Choose a media file", type=[ext[1:] for ext in ALLOWED_EXTENSIONS])

if uploaded_file is not None:
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:
        if ext in {'.mp4', '.avi', '.mov'}:
            st.video(temp_path)
            predictions = classify_video(temp_path, model)
        else:
            img = Image.open(temp_path)
            st.image(img, caption="Uploaded Image", use_column_width=True)
            frame = cv2.imread(temp_path)
            predictions = predict_batch(model, [frame])[0].tolist()

        best_pred = float(np.max(predictions))
        st.write(f"**Prediction Score:** {best_pred:.4f}")
        if best_pred >= 0.5:
            st.error("This appears to be a **Deepfake**.")
        else:
            st.success("This appears to be **Real**.")
        st.json({
            "predictions": predictions,
            "best_prediction": best_pred,
            "classification": "Fake" if best_pred >= 0.5 else "Real"
        })
    except Exception as e:
        st.error(f"Error processing file: {e}")
    finally:
        os.remove(temp_path)
