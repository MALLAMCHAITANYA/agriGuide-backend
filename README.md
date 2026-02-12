# agriGuide Backend (FastAPI)

The **agriGuide Backend** is a FastAPI-based API that powers the crop recommendation and market price features for the agriGuide application.

---

## Features

- **Crop Recommendation API**
  - `POST /predict` – returns the **top 3 recommended crops** based on:
    - Nitrogen (N)
    - Phosphorus (P)
    - Potassium (K)
    - Temperature
    - Humidity
    - Soil pH
    - Rainfall

- **Market Price APIs**
  - `GET /market/price/{crop}` – current price info for a crop.
  - `GET /market/history/{crop}?days=30` – historical price data.
  - `GET /market/stats/{crop}?days=30` – min / max / average prices.
  - `GET /market/trend/{crop}` – simple market trend/forecast.

- **CORS enabled** so the React frontend can call the API from `http://localhost:3000`.

---

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Server:** Uvicorn
- **ML / Data:** scikit-learn, pandas, numpy, joblib
- **Data source:** `data/Crop_recommendation.csv` + trained model (`app/model.pkl`)

---

## Project Structure

backend/
├── app/
│   ├── __init__.py
│   ├── model.pkl              # trained ML model
│   ├── label_encoder.pkl      # label encoder for crop names
│   ├── predict.py             # top‑3 prediction logic
│   ├── schemas.py             # Pydantic request/response models
│   └── market.py              # market price & trend utilities
├── data/
│   └── Crop_recommendation.csv
├── main.py                    # FastAPI entry point (app = FastAPI(...))
├── model_training.py          # script for training the model
├── requirements.txt           # backend Python dependencies
└── .gitignore

Setup & Installation
Clone the repository
git clone https://github.com/<your-username>/agriGuide-backend.gitcd agriGuide-backend
Create and activate a virtual environment (Windows example)
python -m venv myvenvmyvenv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Running the Server
Start the FastAPI server with Uvicorn:
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API root: http://127.0.0.1:8000
Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
Alternative docs (ReDoc): http://127.0.0.1:8000/redoc
Example: Crop Prediction
Endpoint
POST /predictContent-Type: application/json
Request body
{  "N": 90,  "P": 42,  "K": 43,  "temperature": 25.0,  "humidity": 80.0,  "ph": 6.5,  "rainfall": 200.0}
Example response
{  "recommendations": [    { "crop": "rice", "probability": 0.78 },    { "crop": "maize", "probability": 0.15 },    { "crop": "chickpea", "probability": 0.07 }  ]}
Example: Market Price Endpoints
Current price:
GET /market/price/rice
30‑day history:
GET /market/history/rice?days=30
Stats:
GET /market/stats/rice?days=30
Trend:
GET /market/trend/rice
Running Together with Frontend
Start backend: uvicorn main:app --reload --host 127.0.0.1 --port 8000
Start frontend (from frontend/ project): npm start
Configure frontend to call http://127.0.0.1:8000 for API requests.
License
This project is for educational / demonstration purposes.
Feel free to modify and extend it for your own use.
