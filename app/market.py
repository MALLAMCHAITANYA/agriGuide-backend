import random
from datetime import datetime, timedelta


class MarketData:
    def __init__(self):
        # Base market prices for Indian crops (per quintal)
        self.base_prices = {
            "rice": 2500,
            "maize": 1800,
            "chickpea": 5000,
            "kidneybeans": 4500,
            "pigeonpeas": 5500,
            "mothbeans": 4200,
            "mungbean": 6500,
            "blackgram": 6200,
            "lentil": 5800,
            "pomegranate": 8500,
            "banana": 1200,
            "mango": 3000,
            "grapes": 15000,
            "watermelon": 800,
            "muskmelon": 2000,
            "apple": 12000,
            "orange": 2200,
            "papaya": 1500,
            "coconut": 6000,
            "cotton": 5500,
            "jute": 3500,
            "coffee": 45000,
        }

    def get_current_price(self, crop: str):
        """Get current market price with daily variation"""
        crop_lower = crop.lower()
        base = self.base_prices.get(crop_lower, 3000)
        
        # Simulate daily price variation (±5%)
        variation = random.randint(-5, 5)
        current_price = base * (1 + variation / 100)
        
        return {
            "crop": crop,
            "current_price": round(current_price, 2),
            "base_price": base,
            "variation": variation,
            "currency": "INR",
            "unit": "per quintal"
        }

    def get_price_history(self, crop: str, days: int = 30):
        """Get past price history for a crop"""
        crop_lower = crop.lower()
        base = self.base_prices.get(crop_lower, 3000)
        
        prices = []
        current_date = datetime.now()
        
        for i in range(days):
            # Generate realistic price variations day by day
            variation = random.randint(-15, 15)
            price = base * (1 + variation / 100)
            date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            prices.append({
                "date": date,
                "price": round(price, 2)
            })
        
        # Reverse to show oldest first
        return list(reversed(prices))

    def get_price_range_and_stats(self, crop: str, days: int = 30):
        """Get price statistics"""
        history = self.get_price_history(crop, days)
        prices = [h["price"] for h in history]
        
        return {
            "crop": crop,
            "min_price": round(min(prices), 2),
            "max_price": round(max(prices), 2),
            "avg_price": round(sum(prices) / len(prices), 2),
            "current_price": prices[-1],
            "days": len(prices)
        }

    def get_market_trends(self, crop: str):
        """Determine market trend (rising, falling, stable)"""
        history = self.get_price_history(crop, 7)  # Last 7 days
        prices = [h["price"] for h in history]
        
        avg_first_3 = sum(prices[:3]) / 3
        avg_last_3 = sum(prices[-3:]) / 3
        
        change_percent = ((avg_last_3 - avg_first_3) / avg_first_3) * 100
        
        if change_percent > 2:
            trend = "📈 Rising"
        elif change_percent < -2:
            trend = "📉 Falling"
        else:
            trend = "➡️ Stable"
        
        return {
            "crop": crop,
            "trend": trend,
            "change_percent": round(change_percent, 2),
            "forecast": "Good time to sell" if trend == "📈 Rising" else "Good time to buy inputs"
        }
