import os
from functools import lru_cache
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tqdm import tqdm

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST"]}})

# Configuration
MODEL_URL = os.getenv('MODEL_URL')
ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.jpg', '.jpeg', '.png'}
INPUT_SIZE = (128, 128)

@lru_cache(maxsize=1)
def load_model_from_public_s3():
    """Load model from S3 with caching and progress bar."""
    try:
        print("\n🔄 Downloading model from S3...")
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        temp_model_path = 'temp_model.h5'
        
        with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
            with open(temp_model_path, 'wb') as f:
                for data in response.iter_content(chunk_size=8192):  # Increased chunk size
                    size = f.write(data)
                    pbar.update(size)
        
        print("✅ Loading model...")
        model = load_model(temp_model_path)
        os.remove(temp_model_path)
        print("✨ Model loaded successfully!\n")
        return model
    except Exception as e:
        print(f"❌ Error loading model from S3: {e}")
        local_model_path = 'models/cnn_model.h5'
        if os.path.exists(local_model_path):
            print("📂 Loading local model...")
            return load_model(local_model_path)
        raise RuntimeError(f"Failed to load model: {e}")

def preprocess_frame(frame):
    """Preprocess a single frame."""
    return img_to_array(cv2.resize(frame, INPUT_SIZE)) / 255.0

def predict_batch(model, frames, batch_size=32):
    """Make predictions on a batch of frames."""
    preprocessed = np.array([preprocess_frame(frame) for frame in frames])
    return model.predict(preprocessed, batch_size=batch_size, verbose=0)

def classify_video(video_path, model, num_frames=20):
    """Process video with batch predictions."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {video_path}")

    try:
        frames = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = max(1, frame_count // num_frames)

        for i in range(0, frame_count, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret and len(frames) < num_frames:
                frames.append(frame)

        predictions = predict_batch(model, frames)
        return predictions.flatten().tolist()
    finally:
        cap.release()

@app.route("/classify", methods=["POST"])
def classify():
    """Handle classification requests."""
    file = request.files.get("mediaFile")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file format"}), 400

    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        file.save(temp_path)
        
        if ext in {'.mp4', '.avi', '.mov'}:
            predictions = classify_video(temp_path, model)
        else:
            frame = cv2.imread(temp_path)
            if frame is None:
                raise FileNotFoundError("Unable to read image")
            predictions = predict_batch(model, [frame])[0].tolist()

        pred_np = np.array(predictions)
        best_pred = float(pred_np.max())
        
        return jsonify({
            "predictions": predictions,
            "best_prediction": best_pred,
            "classification": "Real" if best_pred < 0.5 else "Fake"
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)

# Initialize model
model = load_model_from_public_s3()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

