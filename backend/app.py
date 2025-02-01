import os
import io
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tqdm import tqdm
import tempfile

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": ["POST"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# S3 configuration
MODEL_URL = os.getenv('MODEL_URL')

# Function to load model from public S3
def load_model_from_public_s3():
    try:
        print("\n🔄 Downloading model from S3...")
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()
        
        # Get file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Save the model temporarily with progress bar
        temp_model_path = 'temp_model.h5'
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        
        with open(temp_model_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                progress_bar.update(size)
        progress_bar.close()
        
        print("✅ Download complete! Loading model...")
        
        # Load the model
        model = load_model(temp_model_path)
        
        # Remove the temporary file
        os.remove(temp_model_path)
        
        print("✨ Model loaded successfully!\n")
        return model
    except Exception as e:
        print(f"❌ Error loading model from S3: {e}")
        # Fallback to local model if available
        local_model_path = 'models/cnn_model.h5'
        if os.path.exists(local_model_path):
            print("📂 Loading local model as fallback...")
            model = load_model(local_model_path)
            print("✅ Local model loaded successfully!\n")
            return model
        raise RuntimeError(f"Failed to load model: {e}")

# Load the model
model = load_model_from_public_s3()

# Function to preprocess a frame or image
def preprocess_frame(frame):
    try:
        frame_resized = cv2.resize(frame, (128, 128))
        frame_normalized = img_to_array(frame_resized) / 255.0
        return np.expand_dims(frame_normalized, axis=0)
    except Exception as e:
        raise ValueError(f"Error preprocessing frame: {e}")

# Analyze predictions
def analyze_predictions(predictions):
    predictions_np = np.array(predictions, dtype=np.float64)
    best_prediction = float(max(predictions_np))
    classification = "Real" if best_prediction < 0.5 else "Fake"
    return predictions_np, best_prediction, classification

# Process video and classify frames
def classify_video(video_path, model, num_frames=20):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video file: {video_path}")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, frame_count // num_frames)
    predictions = []

    frame_idx = 0
    while cap.isOpened() and len(predictions) < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            try:
                preprocessed_frame = preprocess_frame(frame)
                prediction = float(model.predict(preprocessed_frame, verbose=0)[0][0])
                predictions.append(prediction)
            except Exception as e:
                print(f"Error predicting frame at index {frame_idx}: {e}")
        frame_idx += 1

    cap.release()
    return predictions

# Process photo and classify
def classify_photo(photo_path, model):
    try:
        frame = cv2.imread(photo_path)
        if frame is None:
            raise FileNotFoundError(f"Unable to read image: {photo_path}")
        preprocessed_frame = preprocess_frame(frame)
        prediction = float(model.predict(preprocessed_frame, verbose=0)[0][0])
        return [prediction]
    except Exception as e:
        raise RuntimeError(f"Error processing image: {e}")

@app.route("/classify", methods=["POST"])
def classify():
    file = request.files.get("mediaFile")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save file temporarily using a secure filename
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)
        print(f"File saved temporarily at: {temp_file_path}")

        if file.filename.lower().endswith((".mp4", ".avi", ".mov")):
            predictions = classify_video(temp_file_path, model)
        elif file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            predictions = classify_photo(temp_file_path, model)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        predictions_np, best_prediction, classification = analyze_predictions(predictions)

        return jsonify({
            "predictions": predictions_np.tolist(),
            "best_prediction": best_prediction,
            "classification": classification,
        })
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up: delete the temporary file and directory
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                os.rmdir(temp_dir)
        except Exception as e:
            print(f"Error cleaning up temporary files: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

