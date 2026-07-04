"""
Market Prices Tool – AgriSense AI
───────────────────────────────────
Placeholder for real-time mandi/commodity prices.

Future integration:
  - Agmarknet API (data.gov.in)
  - e-NAM platform data
  - NCDEX / MCX commodity prices
  - MSP (Minimum Support Price) database from CACP
"""

from datetime import date


def get_market_prices(crop: str = None, state: str = None) -> dict:
    """
    Fetch current market prices for agricultural commodities.

    Args:
        crop (str, optional): Specific crop name to filter (e.g., "Wheat")
        state (str, optional): State to filter mandi prices

    Returns:
        dict: Market prices with trend indicators and MSP comparison.

    TODO: Replace stub with real API:
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {"api-key": os.getenv("AGMARKNET_API_KEY"), "format": "json"}
    """
    today = date.today().isoformat()

    all_prices = [
        {"crop": "Wheat", "variety": "Sharbati", "market": "Bhopal", "state": "Madhya Pradesh",
         "min_price": 2100, "max_price": 2350, "modal_price": 2250, "msp": 2275, "trend": "up", "unit": "₹/quintal"},
        {"crop": "Rice", "variety": "Common", "market": "Hyderabad", "state": "Telangana",
         "min_price": 1800, "max_price": 2100, "modal_price": 1950, "msp": 2183, "trend": "stable", "unit": "₹/quintal"},
        {"crop": "Cotton", "variety": "H4", "market": "Nagpur", "state": "Maharashtra",
         "min_price": 5500, "max_price": 6200, "modal_price": 5850, "msp": 6620, "trend": "down", "unit": "₹/quintal"},
        {"crop": "Soybean", "variety": "Yellow", "market": "Indore", "state": "Madhya Pradesh",
         "min_price": 3800, "max_price": 4300, "modal_price": 4050, "msp": 4600, "trend": "up", "unit": "₹/quintal"},
        {"crop": "Maize", "variety": "Hybrid", "market": "Davangere", "state": "Karnataka",
         "min_price": 1650, "max_price": 1950, "modal_price": 1800, "msp": 2090, "trend": "up", "unit": "₹/quintal"},
        {"crop": "Tomato", "variety": "Local", "market": "Nashik", "state": "Maharashtra",
         "min_price": 800, "max_price": 1500, "modal_price": 1100, "msp": None, "trend": "up", "unit": "₹/quintal"},
        {"crop": "Onion", "variety": "Red", "market": "Lasalgaon", "state": "Maharashtra",
         "min_price": 600, "max_price": 1200, "modal_price": 900, "msp": None, "trend": "stable", "unit": "₹/quintal"},
        {"crop": "Potato", "variety": "Jyoti", "market": "Agra", "state": "Uttar Pradesh",
         "min_price": 700, "max_price": 1000, "modal_price": 850, "msp": None, "trend": "down", "unit": "₹/quintal"},
        {"crop": "Mustard", "variety": "T-9", "market": "Alwar", "state": "Rajasthan",
         "min_price": 4900, "max_price": 5400, "modal_price": 5150, "msp": 5650, "trend": "up", "unit": "₹/quintal"},
        {"crop": "Chickpea", "variety": "Desi", "market": "Kota", "state": "Rajasthan",
         "min_price": 4700, "max_price": 5200, "modal_price": 4950, "msp": 5440, "trend": "stable", "unit": "₹/quintal"},
        {"crop": "Sugarcane", "variety": "Co-86032", "market": "Pune", "state": "Maharashtra",
         "min_price": 2800, "max_price": 3200, "modal_price": 3050, "msp": 3150, "trend": "stable", "unit": "₹/tonne"},
        {"crop": "Groundnut", "variety": "Bold", "market": "Rajkot", "state": "Gujarat",
         "min_price": 5200, "max_price": 5900, "modal_price": 5550, "msp": 6377, "trend": "down", "unit": "₹/quintal"},
    ]

    if crop:
        filtered = [p for p in all_prices if p["crop"].lower() == crop.lower()]
        prices = filtered if filtered else all_prices
    elif state:
        filtered = [p for p in all_prices if p["state"].lower() == state.lower()]
        prices = filtered if filtered else all_prices
    else:
        prices = all_prices

    return {
        "date": today,
        "prices": prices,
        "total_records": len(prices),
        "source": "stub",  # change to "agmarknet" when live
        "disclaimer": "Prices are indicative. Verify at your local mandi before selling.",
    }
