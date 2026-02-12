from pydantic import BaseModel
from typing import List


class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class CropPrediction(BaseModel):
    crop: str
    probability: float


class PredictionResponse(BaseModel):
    recommendations: List[CropPrediction]
