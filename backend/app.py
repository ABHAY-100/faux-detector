from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins
        "methods": ["POST"],  # Only allow POST requests
        "allow_headers": ["Content-Type", "Authorization"]  # Include necessary headers
    }
})

# Paths to model
MODEL_PATH = 'cnn_model.h5'
# https://www.dropbox.com/scl/fi/0zh88gmiw79j6wozdzhxe/cnn_model.h5?rlkey=oh0g202fnkssq0r1imlz0u4s3&st=aahgdn49&dl=0

dropbox_url = "https://www.dropbox.com/scl/fi/0zh88gmiw79j6wozdzhxe/cnn_model.h5?rlkey=oh0g202fnkssq0r1imlz0u4s3&st=aahgdn49&dl=0"

# Download the model
response = request.get(dropbox_url)
with open("model.h5", "wb") as f:
    f.write(response.content)

# Load the trained model
try:
    model = load_model("model.h5")
    print("Model loaded successfully.")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

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
    predictions_np = np.array(predictions, dtype=np.float64)  # Ensure float64 for JSON compatibility
    best_prediction = float(max(predictions_np))  # Convert to native float
    classification = 'Real' if best_prediction < 0.5 else 'Fake'
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
                prediction = float(model.predict(preprocessed_frame, verbose=0)[0][0])  # Convert to native float
                predictions.append(prediction)
            except Exception as e:
                print(f"Error predicting frame at index {frame_idx}: {e}")
        frame_idx += 1

    cap.release()
    return predictions

# Process photo and classify
# Process photo and classify
def classify_photo(photo_path, model):
    try:
        frame = cv2.imread(photo_path)  # Correctly assign the read image to 'frame'
        if frame is None:
            raise FileNotFoundError(f"Unable to read image: {photo_path}")
        preprocessed_frame = preprocess_frame(frame)
        prediction = float(model.predict(preprocessed_frame, verbose=0)[0][0])  # Convert to native float
        return [prediction]
    except Exception as e:
        raise RuntimeError(f"Error processing image: {e}")

@app.route('/classify', methods=['POST'])
def classify():
    file = request.files.get('mediaFile')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = f"temp_{file.filename}"
    file.save(file_path)

    try:
        if file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            predictions = classify_video(file_path, model)
        elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            predictions = classify_photo(file_path, model)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        predictions_np, best_prediction, classification = analyze_predictions(predictions)

        return jsonify({
            "predictions": predictions_np.tolist(),  # Convert NumPy array to list
            "best_prediction": best_prediction,
            "classification": classification
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
