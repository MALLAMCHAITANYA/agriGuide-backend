from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.predict import predict_top3
from app.schemas import CropInput, PredictionResponse
from app.market import MarketData

app = FastAPI(title="Crop Recommendation System")

# Initialize market service
market_service = MarketData()

# -------------------------------------------------
# Enable CORS
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Crop Prediction API (Top-3)
# -------------------------------------------------
@app.post("/predict", response_model=PredictionResponse)
async def predict(data: CropInput):

    input_data = [[
        data.N,
        data.P,
        data.K,
        data.temperature,
        data.humidity,
        data.ph,
        data.rainfall
    ]]

    results = predict_top3(input_data)

    return {
        "recommendations": results
    }

# -------------------------------------------------
# Market Price API
# -------------------------------------------------
@app.get("/market/price/{crop}")
def get_market_price(crop: str):
    """Get current market price for a crop"""
    return market_service.get_current_price(crop)

@app.get("/market/history/{crop}")
def get_price_history(crop: str, days: int = 30):
    """Get historical price data for a crop"""
    return {
        "crop": crop,
        "history": market_service.get_price_history(crop, days)
    }

@app.get("/market/stats/{crop}")
def get_price_stats(crop: str, days: int = 30):
    """Get price statistics"""
    return market_service.get_price_range_and_stats(crop, days)

@app.get("/market/trend/{crop}")
def get_market_trend(crop: str):
    """Get market trend and forecast"""
    return market_service.get_market_trends(crop)

# -------------------------------------------------
# Root Endpoint
# -------------------------------------------------
@app.get("/")
def home():
    return {"message": "Crop Recommendation API Running!"}
