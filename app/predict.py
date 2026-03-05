import os
import joblib
import numpy as np
import pandas as pd

# Get app directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# Global variables for model and encoder (lazy loading)
model = None
label_encoder = None

def load_predictor():
    """Load model and encoder only when needed"""
    global model, label_encoder
    if model is None:
        print(f"DEBUG: Starting to load model from {MODEL_PATH}...", flush=True)
        model = joblib.load(MODEL_PATH)
        print("DEBUG: Model loaded successfully.", flush=True)
    if label_encoder is None:
        print(f"DEBUG: Starting to load label encoder from {ENCODER_PATH}...", flush=True)
        label_encoder = joblib.load(ENCODER_PATH)
        print("DEBUG: Label encoder loaded successfully.", flush=True)


def predict_top3(input_data):
    """
    input_data: [[N, P, K, temperature, humidity, ph, rainfall]]
    """
    # Ensure model is loaded
    load_predictor()
    
    # Convert list to DataFrame with correct column names
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    df_input = pd.DataFrame(input_data, columns=features)

    probs = model.predict_proba(df_input)[0]
    top_indices = np.argsort(probs)[-3:][::-1]

    crops = label_encoder.inverse_transform(top_indices)

    results = []
    for crop, prob in zip(crops, probs[top_indices]):
        results.append({
            "crop": crop,
            "probability": round(float(prob), 4)
        })

    return results
