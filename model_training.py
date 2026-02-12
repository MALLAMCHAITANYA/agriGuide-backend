import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# =====================================================
# 🔹 CORRECT PATH HANDLING (DATASET IN BACKEND FOLDER)
# =====================================================

# backend directory (where this file exists)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset path (same folder as model_training.py)
DATA_PATH = os.path.join(BASE_DIR, "data", "Crop_recommendation.csv")


# Model save directory (FastAPI app folder)
MODEL_DIR = os.path.join(BASE_DIR, "app")
os.makedirs(MODEL_DIR, exist_ok=True)

print("📁 Dataset path:", DATA_PATH)
print("📁 Model directory:", MODEL_DIR)

# =====================================================
# 🔹 LOAD DATASET
# =====================================================

df = pd.read_csv(DATA_PATH)

# Features & Target
features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
target = 'label'

X = df[features]
y = df[target]

# =====================================================
# 🔹 LABEL ENCODING
# =====================================================

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save label encoder
joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))

# =====================================================
# 🔹 PREPROCESSING + MODEL PIPELINE
# =====================================================

preprocess = ColumnTransformer(
    transformers=[
        ('scale', StandardScaler(), features)
    ]
)

model = Pipeline(steps=[
    ('preprocess', preprocess),
    ('classifier', RandomForestClassifier(
        n_estimators=400,
        random_state=42
    ))
])

# =====================================================
# 🔹 TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# =====================================================
# 🔹 TRAIN MODEL
# =====================================================

model.fit(X_train, y_train)

# =====================================================
# 🔹 EVALUATION
# =====================================================

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n🌱 Model Training Completed Successfully!")
print(f"🎯 Accuracy: {accuracy * 100:.2f}%\n")
print("📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# =====================================================
# 🔹 SAVE TRAINED MODEL
# =====================================================

joblib.dump(model, os.path.join(MODEL_DIR, "model.pkl"))

print("💾 Model saved successfully inside:", MODEL_DIR)
