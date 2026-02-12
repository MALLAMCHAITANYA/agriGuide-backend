import os
import joblib
import numpy as np
import pandas as pd

# Get app directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# Load trained model & label encoder
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


def predict_top3(input_data):
    """
    input_data: [[N, P, K, temperature, humidity, ph, rainfall]]
    """
    
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
