import json
import os
import random
from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import urlopen


class MarketData:
    def __init__(self):
        self.api_key = os.getenv("DATA_GOV_API_KEY", "")
        self.resource_id = os.getenv(
            "DATA_GOV_RESOURCE_ID",
            "9ef84268-d588-465a-a308-a864a43d0070",
        )
        self.base_url = f"https://api.data.gov.in/resource/{self.resource_id}"
        self.cache_ttl_seconds = 15 * 60
        self._records_cache = {}

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
            "potato": 1200,
            "onion": 1500,
            "tomato": 2000,
            "mustard": 5000,
            "soybean": 4500,
            "sugarcane": 300,
            "garlic": 8000,
            "turmeric": 7000,
            "ginger": 6000,
        }

        self.crop_to_commodity = {
            "rice": "Rice",
            "maize": "Maize",
            "chickpea": "Gram",
            "kidneybeans": "Rajma",
            "pigeonpeas": "Arhar",
            "mothbeans": "Moth",
            "mungbean": "Moong",
            "blackgram": "Urad",
            "lentil": "Masur",
            "pomegranate": "Pomegranate",
            "banana": "Banana",
            "mango": "Mango",
            "grapes": "Grapes",
            "watermelon": "Water Melon",
            "muskmelon": "Musk Melon",
            "apple": "Apple",
            "orange": "Orange",
            "papaya": "Papaya",
            "coconut": "Coconut",
            "cotton": "Cotton",
            "jute": "Jute",
            "coffee": "Coffee",
            "potato": "Potato",
            "onion": "Onion",
            "tomato": "Tomato",
            "mustard": "Mustard",
            "soybean": "Soyabean",
            "sugarcane": "Sugarcane",
            "garlic": "Garlic",
            "turmeric": "Turmeric",
            "ginger": "Ginger",
        }

    def _parse_price(self, value):
        if value is None:
            return None
        try:
            return float(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return None

    def _parse_date(self, value):
        if not value:
            return None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

    def _fetch_datagov_records(self, crop: str, limit: int = 90):
        commodity = self.crop_to_commodity.get(crop.lower())
        if not commodity or not self.api_key:
            return []

        cache_key = f"{commodity}:{limit}"
        cached = self._records_cache.get(cache_key)
        if cached:
            age = (datetime.now() - cached["time"]).total_seconds()
            if age < self.cache_ttl_seconds:
                return cached["records"]

        params = {
            "api-key": self.api_key,
            "format": "json",
            "limit": str(limit),
            "filters[commodity]": commodity,
            "sort": "arrival_date desc",
        }

        try:
            url = f"{self.base_url}?{urlencode(params)}"
            with urlopen(url, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if isinstance(payload, dict):
                records = payload.get("records", [])
            else:
                records = []
            self._records_cache[cache_key] = {"time": datetime.now(), "records": records}
            return records
        except Exception:
            return []

    def _get_live_records(self, crop: str, days: int = 30):
        rows = self._fetch_datagov_records(crop, max(days * 4, 60))
        parsed = []

        for row in rows:
            # Handle both uppercase and lowercase field names
            price = self._parse_price(row.get("Modal_Price") or row.get("modal_price"))
            arrival = row.get("Arrival_Date") or row.get("arrival_date")
            parsed_date = self._parse_date(arrival)
            
            if price is None or parsed_date is None:
                continue

            parsed.append(
                {
                    "date": parsed_date,
                    "price": price,
                    "state": row.get("State") or row.get("state"),
                    "district": row.get("District") or row.get("district"),
                    "market": row.get("Market") or row.get("market"),
                    "commodity": row.get("Commodity") or row.get("commodity"),
                }
            )

        parsed.sort(key=lambda item: item["date"])
        return parsed

    def _simulated_current_price(self, crop: str):
        crop_lower = crop.lower()
        base = self.base_prices.get(crop_lower, 3000)
        
        # Use crop name and current date as a seed for consistency
        seed_str = f"{crop_lower}:{datetime.now().strftime('%Y-%m-%d')}"
        rng = random.Random(seed_str)
        variation = rng.randint(-5, 5)
        current_price = base * (1 + variation / 100)

        return {
            "crop": crop,
            "current_price": round(current_price, 2),
            "base_price": base,
            "variation": variation,
            "currency": "INR",
            "unit": "per quintal",
            "source": "simulated",
        }

    def get_current_price(self, crop: str):
        live_rows = self._get_live_records(crop, days=30)
        if not live_rows:
            return self._simulated_current_price(crop)

        latest = live_rows[-1]
        lookback = live_rows[-7:] if len(live_rows) >= 7 else live_rows
        avg_recent = sum(item["price"] for item in lookback) / len(lookback)
        variation = ((latest["price"] - avg_recent) / avg_recent) * 100 if avg_recent else 0

        return {
            "crop": crop,
            "current_price": round(latest["price"], 2),
            "base_price": round(avg_recent, 2),
            "variation": round(variation, 2),
            "currency": "INR",
            "unit": "per quintal",
            "source": "data.gov.in",
            "market": latest.get("market"),
            "district": latest.get("district"),
            "state": latest.get("state"),
            "last_updated": latest["date"].strftime("%Y-%m-%d"),
        }

    def get_price_history(self, crop: str, days: int = 30):
        live_rows = self._get_live_records(crop, days=days)
        if live_rows:
            return [
                {
                    "date": row["date"].strftime("%Y-%m-%d"),
                    "price": round(row["price"], 2),
                }
                for row in live_rows[-days:]
            ]

        crop_lower = crop.lower()
        base = self.base_prices.get(crop_lower, 3000)
        prices = []
        current_date = datetime.now()

        for i in range(days):
            date_obj = current_date - timedelta(days=i)
            date_str = date_obj.strftime("%Y-%m-%d")
            
            # Consistent seed per day/crop
            seed_str = f"{crop_lower}:{date_str}"
            rng = random.Random(seed_str)
            
            variation = rng.randint(-15, 15)
            price = base * (1 + variation / 100)
            prices.append({"date": date_str, "price": round(price, 2)})

        return list(reversed(prices))

    def get_price_range_and_stats(self, crop: str, days: int = 30):
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
            "forecast": "Good time to sell"
            if trend == "📈 Rising"
            else "Good time to buy inputs",
        }
