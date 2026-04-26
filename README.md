# ⚙️ AgriGuide - Backend (Intelligence Hub)

**[🔗 View Live Demo](https://agriguide-web.vercel.app/)**

The **AgriGuide Backend** is the high-performance engine that powers our AI-driven agricultural solutions. Built with scalability and accuracy in mind, it handles complex Machine Learning inferences and real-time market data aggregation.

---

## 🧠 AI & Intelligence

At the heart of the system is a **Random Forest Classifier** model trained on high-fidelity Soil and Climate datasets. 

*   **Input Parameters**: Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH Value, and Rainfall.
*   **Recommendation Model**: Predicts the top 3 most suitable crops with confidence scores.
*   **Market Intelligence**: Aggregates commodity prices from data APIs and calculates trends, forecasts, and demand levels.

---

## ✨ Core Features

*   **⚡ High-Performance API**: Powered by **FastAPI** for near-instant response times.
*   **📊 Market Logic**: Custom algorithms to process price history and generate "Rising," "Falling," or "Stable" trend signals.
*   **🛡️ Robust Security**: Pre-configured CORS middleware for secure integration with Vercel and other frontend platforms.
*   **📝 Auto-Documentation**: Integrated Swagger UI (`/docs`) for easy API testing and developer collaboration.

---

## 🛠️ Tech Stack

*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Language**: Python 3.9+
*   **Machine Learning**: Scikit-Learn, Joblib
*   **Data Processing**: Pandas, NumPy
*   **Server**: Uvicorn (ASGI)

---

## 🚀 Quick Setup

### 1. Environment Setup
Create and activate a virtual environment:
```bash
python -m venv myvenv
# Windows
myvenv\Scripts\activate
# Mac/Linux
source myvenv/bin/activate
```

### 2. Dependency Management
Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Launch the Hub
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Visit `http://localhost:8000/docs` to test the API endpoints interactively.

---

## 🏗️ Production Deployment (Render)

1. Create a **Web Service** on Render.
2. Select your repository and set the **Root Directory** to `backend`.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Render will automatically handle SSL and provide a secure HTTPS endpoint.

---

## 📈 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/predict` | Get Top-3 crop recommendations from soil inputs. |
| `GET` | `/market/price/{crop}` | Get current market price & location data. |
| `GET` | `/market/trend/{crop}` | Get price forecasts and market sentiment. |
| `GET` | `/` | Health check and server status. |

---
*Providing the logic behind smarter farming.* 🚜
