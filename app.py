"""
AgriSense AI – Main Flask Application
========================================
IBM watsonx.ai + IBM Granite foundation model powered smart farming advisor.
"""

import os
import json
import markdown
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from flask import request
try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False
    Credentials = ModelInference = GenParams = None

# ── Tool imports (placeholder functions ready for real data) ──────
from tools.weather_tool import get_weather_data
from tools.crop_tool import get_crop_recommendation
from tools.market_tool import get_market_prices
from tools.scheme_tool import get_government_schemes
from tools.soil_tool import get_soil_information
from tools.pest_tool import get_pest_management

# ── Agent instructions (edit agent_instructions.py to customize) ──
from agent_instructions import SYSTEM_PROMPT, AGENT_NAME

# ─────────────────────────────────────────────────────────────────
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "agrisense-dev-secret-change-me")

# ─────────────────────────────────────────────────────────────────
#  IBM watsonx.ai Configuration
# ─────────────────────────────────────────────────────────────────
IBM_API_KEY = os.getenv("IBM_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# IBM Granite model – change to any supported Granite model ID
GRANITE_MODEL_ID = "ibm/granite-3-8b-instruct"

# Generation parameters – tune these for desired response style
GENERATION_PARAMS = {
    "max_new_tokens": 800,
    "min_new_tokens": 30,
    "temperature": 0.3,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.1,
    "stop_sequences": ["<|endoftext|>", "Human:", "User:"],
}


def get_watsonx_model():
    """
    Initialize and return the IBM watsonx.ai ModelInference client.
    Returns None if credentials are missing or library not installed (demo mode).
    """
    if not WATSONX_AVAILABLE or not IBM_API_KEY or not WATSONX_PROJECT_ID:
        return None
    try:
        credentials = Credentials(url=WATSONX_URL, api_key=IBM_API_KEY)
        model = ModelInference(
            model_id=GRANITE_MODEL_ID,
            credentials=credentials,
            project_id=WATSONX_PROJECT_ID,
            params=GENERATION_PARAMS,
        )
        return model
    except Exception as e:
        app.logger.error(f"watsonx.ai init error: {e}")
        return None


def build_prompt(conversation_history: list, user_message: str) -> str:
    """
    Build the chat prompt in IBM Granite's expected format.
    Includes system prompt from agent_instructions.py and conversation history.
    
    Format: <|system|>...<|user|>...<|assistant|>
    This format is for granite-13b-chat-v2 and similar Granite chat models.
    Adjust the template if using a different model family.
    """
    prompt_parts = [f"<|system|>\n{SYSTEM_PROMPT}\n"]

    # Include last N turns of history to stay within context window
    MAX_HISTORY_TURNS = 5
    recent_history = conversation_history[-MAX_HISTORY_TURNS * 2:]

    for msg in recent_history:
        if msg["role"] == "user":
            prompt_parts.append(f"<|user|>\n{msg['content']}\n")
        elif msg["role"] == "assistant":
            prompt_parts.append(f"<|assistant|>\n{msg['content']}\n")

    prompt_parts.append(f"<|user|>\n{user_message}\n<|assistant|>\n")
    return "".join(prompt_parts)


def generate_response(user_message: str, conversation_history: list) -> dict:
    """
    Generate an AI response using IBM Granite via watsonx.ai.
    Falls back to a demo response if credentials are not configured.

    Args:
        user_message: The user's input text
        conversation_history: List of {"role": "user"|"assistant", "content": str}

    Returns:
        dict with keys: text (str), tokens_used (int), model (str), mode (str)
    """
    model = get_watsonx_model()

    if model is None:
        # ── DEMO MODE (no credentials configured) ─────────────────
        demo_response = generate_demo_response(user_message)
        return {
            "text": demo_response,
            "tokens_used": 0,
            "model": "demo-mode",
            "mode": "demo",
        }

    try:
        prompt = build_prompt(conversation_history, user_message)
        result = model.generate_text(prompt=prompt)
        print("=" * 60)
        print("USER MESSAGE:")
        print(user_message)

        print("=" * 60)
        print("PROMPT:")
        print(prompt)

        print("=" * 60)
        print("RAW MODEL OUTPUT:")
        print(result)
        print("=" * 60)

        response_text = result if isinstance(result, str) else str(result)
        response_text = response_text.strip()

        # Clean up any leftover stop sequences
        for stop_seq in ["<|endoftext|>", "Human:", "User:", "<|user|>", "<|system|>"]:
            if stop_seq in response_text:
                response_text = response_text.split(stop_seq)[0].strip()

        return {
            "text": response_text,
            "tokens_used": len(response_text.split()),  # approximate
            "model": GRANITE_MODEL_ID,
            "mode": "watsonx",
        }

    except Exception as e:
        app.logger.error(f"Generation error: {e}")
        return {
            "text": (
                "🌾 I'm having trouble connecting to the AI service right now. "
                "Please check your IBM watsonx.ai credentials in the `.env` file and try again.\n\n"
                f"**Error:** {str(e)}"
            ),
            "tokens_used": 0,
            "model": GRANITE_MODEL_ID,
            "mode": "error",
        }


def generate_demo_response(user_message: str) -> str:
    """
    Rule-based demo responses for when watsonx.ai credentials are not configured.
    Demonstrates the application without requiring live API keys.
    """
    msg_lower = user_message.lower()

    if any(kw in msg_lower for kw in ["weather", "rain", "temperature", "forecast"]):
        return (
            "🌤️ **Current Weather Advisory**\n\n"
            "Based on typical conditions this season:\n\n"
            "- 🌡️ **Temperature:** 28–32°C (ideal for Kharif crops)\n"
            "- 💧 **Humidity:** 70–75% (good for rice, moderate for cotton)\n"
            "- 🌧️ **Rainfall forecast:** Moderate showers expected mid-week\n"
            "- ☀️ **UV Index:** High — avoid spraying between 11am–3pm\n\n"
            "**Farming Tip:** Hold irrigation for 2 days if rain is expected. "
            "Ensure proper drainage in low-lying fields to prevent waterlogging. 🌾\n\n"
            
        )

    if any(kw in msg_lower for kw in ["crop", "plant", "grow", "sow", "cultivat"]):
        return (
            "🌱 **Crop Recommendation**\n\n"
            "Based on the current Kharif season and general soil conditions:\n\n"
            "**Top Recommended Crops:**\n"
            "1. 🌾 **Rice (Paddy)** – Suitability: 90% | Water: High\n"
            "2. 🌽 **Maize** – Suitability: 85% | Water: Medium\n"
            "3. 🫘 **Soybean** – Suitability: 82% | Water: Low\n"
            "4. 🌻 **Sunflower** – Suitability: 78% | Water: Low\n\n"
            "**Quick Tips:**\n"
            "- Get your **Soil Health Card** to fine-tune fertilizer doses\n"
            "- Use **certified seeds** from government-approved sources\n"
            "- Follow **line sowing** for better yields and mechanized harvesting\n\n"
            "Would you like advice on fertilizer scheduling or irrigation for any of these crops? 🌿"
        )

    if any(kw in msg_lower for kw in ["price", "market", "mandi", "sell", "rate", "msp"]):
        return (
            "📊 **Today's Market Prices (Sample)**\n\n"
            "| Crop | Modal Price | MSP | Trend |\n"
            "|------|-------------|-----|-------|\n"
            "| Wheat | ₹2,250/qtl | ₹2,275 | 📈 Up |\n"
            "| Rice | ₹1,950/qtl | ₹2,183 | ➡️ Stable |\n"
            "| Soybean | ₹4,050/qtl | ₹4,600 | 📈 Up |\n"
            "| Cotton | ₹5,850/qtl | ₹6,620 | 📉 Down |\n\n"
            "💡 **Tip:** Prices at **e-NAM** (enam.gov.in) often offer better rates "
            "than local mandis due to wider buyer reach.\n\n"
            "Which crop price would you like more details on?"
        )

    if any(kw in msg_lower for kw in ["scheme", "subsidy", "government", "yojana", "kisan", "pm-kisan"]):
        return (
            "🏛️ **Key Government Schemes for Farmers**\n\n"
            "**1. PM-KISAN** 💰\n"
            "₹6,000/year in 3 installments — Apply at pmkisan.gov.in\n\n"
            "**2. PM Fasal Bima Yojana** 🛡️\n"
            "Crop insurance at 1.5–2% premium — Apply through your bank\n\n"
            "**3. Kisan Credit Card (KCC)** 💳\n"
            "Crop loans at just 4% interest — Visit any nationalized bank\n\n"
            "**4. Soil Health Card** 🧪\n"
            "Free soil testing every 2 years — Contact nearest KVK\n\n"
            "**5. PM Krishi Sinchayee Yojana** 💧\n"
            "Up to 55% subsidy on drip/sprinkler irrigation\n\n"
            "Would you like details on how to apply for any of these schemes?"
        )

    if any(kw in msg_lower for kw in ["pest", "disease", "insect", "fungus", "spray", "infection"]):
        return (
            "🐛 **Pest & Disease Management Advisory**\n\n"
            "**Integrated Pest Management (IPM) Approach:**\n\n"
            "**Step 1 – Scout Your Field:**\n"
            "Walk your field twice a week. Check leaf undersides, stems, and soil near roots.\n\n"
            "**Step 2 – Identify the Problem:**\n"
            "- 🟡 Yellow leaves → Possible nitrogen deficiency or viral disease\n"
            "- 🍂 Brown spots → Fungal infection (check for spores)\n"
            "- 🕳️ Holes in leaves → Caterpillar or beetle damage\n\n"
            "**Step 3 – IPM Response:**\n"
            "1. **Cultural:** Remove infected plants, improve drainage\n"
            "2. **Biological:** Neem oil (3ml/liter), Trichoderma for soil\n"
            "3. **Chemical:** Only if above ETL — wear full PPE\n\n"
            "⚠️ **Safety:** Always follow PHI (Pre-Harvest Interval) on pesticide labels.\n\n"
            "📞 Kisan Call Centre: **1800-180-1551** (Toll Free)\n\n"
            "What crop and symptoms are you dealing with?"
        )

    if any(kw in msg_lower for kw in ["soil", "ph", "nutrient", "fertilizer", "organic", "manure"]):
        return (
            "🧪 **Soil Health & Fertilizer Guide**\n\n"
            "**General NPK Recommendation (per acre):**\n\n"
            "| Crop | Nitrogen (N) | Phosphorus (P) | Potassium (K) |\n"
            "|------|-------------|----------------|---------------|\n"
            "| Wheat | 120 kg Urea | 50 kg DAP | 25 kg MOP |\n"
            "| Rice | 100 kg Urea | 40 kg SSP | 20 kg MOP |\n"
            "| Maize | 130 kg Urea | 60 kg DAP | 30 kg MOP |\n\n"
            "**Organic Farming Tips:**\n"
            "- 🌿 Apply **FYM (Farm Yard Manure)** @ 5 tonnes/acre\n"
            "- 🪱 **Vermicompost** @ 2 tonnes/acre improves soil structure\n"
            "- 🌱 **Green Manure** (Dhaincha/Sunhemp) before paddy sowing\n\n"
            "💡 Always get a **Soil Health Card** before fertilizing — it saves 15–20% input cost!\n\n"
            "What specific crop or soil problem would you like advice on?"
        )
    
    if any(kw in msg_lower for kw in ["irrigation", "drip", "sprinkler", "water", "water-scarce","drought", "watering", "irrigate"]):
      return (
        "💧 **Irrigation Advisory**\n\n"
        "**For water-scarce regions, drip irrigation is the most efficient method.**\n\n"
        "Benefits:\n"
        "- 💦 Saves up to 50–70% water\n"
        "- 🌱 Delivers water directly to plant roots\n"
        "- 🌾 Improves crop yield and fertilizer efficiency\n"
        "- 🌞 Reduces evaporation and weed growth\n\n"
        "**Suitable Crops:** Cotton, vegetables, fruits, sugarcane and horticultural crops.\n\n"
        "💡 Tip: Farmers can also explore government subsidies under the **PM Krishi Sinchayee Yojana** for drip irrigation systems."
    )

    # Default / General response
    return (
        f"🌾 **Welcome to {AGENT_NAME}!**\n\n"
        "I'm your intelligent farming advisor, powered by IBM Granite AI. "
        "I can help you with:\n\n"
        "- 🌱 **Crop recommendations** based on your soil and season\n"
        "- 🌦️ **Weather-based farming advice**\n"
        "- 🧪 **Soil health and fertilizer guidance**\n"
        "- 🐛 **Pest and disease management** (IPM approach)\n"
        "- 💧 **Irrigation scheduling**\n"
        "- 📊 **Market prices** and best time to sell\n"
        "- 🏛️ **Government schemes** and how to apply\n\n"
        "**Try asking me:**\n"
        "*\"What crops should I grow this Kharif season on black soil?\"*\n"
        "*\"How do I treat wheat rust disease?\"*\n"
        "*\"What is the MSP of rice this year?\"*\n\n"
        "I support English and major Indian regional languages. "
        "How can I help you today? 🙏"
    )



# ─────────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Homepage – Hero, Features, Stats, CTA"""
    return render_template("index.html")


@app.route("/chat")
def chat():
    """Chat page – Conversational AI interface"""
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("chat.html", chat_history=session.get("chat_history", []))


@app.route("/dashboard")
def dashboard():
    """Dashboard – Overview of weather, crops, market, soil"""
    weather = get_weather_data("Nashik")
    market = get_market_prices()
    soil = get_soil_information(soil_type="black")
    crops = get_crop_recommendation("black", "kharif", "Maharashtra")
    return render_template(
        "dashboard.html",
        weather=weather,
        market_prices=market["prices"][:6],
        soil=soil,
        crops=crops,
    )


@app.route("/weather")
def weather():

    city = request.args.get("city")

    if city:
        # User searched for a city
        weather_data = {
            city: get_weather_data(city)
        }

    else:
        # Default cities shown on first load
        default_cities = [
            "Ludhiana",
            "Delhi",
            "Hyderabad",
            "Pune",
            "Jaipur",
            "Bengaluru"
        ]

        weather_data = {}

        for c in default_cities:
            weather_data[c] = get_weather_data(c)

    return render_template(
        "weather.html",
        weather_data=weather_data,
        selected_city=city if city else ""
    )


@app.route("/market")
def market():
    """Market prices page"""
    prices = get_market_prices()
    return render_template("market.html", market_data=prices)


@app.route("/schemes")
def schemes():
    """Government schemes page"""
    schemes_data = get_government_schemes()
    return render_template("schemes.html", schemes=schemes_data)


# ─────────────────────────────────────────────────────────────────
#  API ENDPOINTS
# ─────────────────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Main chat API endpoint.
    Accepts: { "message": str, "history": list (optional) }
    Returns: { "response": str, "html_response": str, "meta": dict }
    """
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if len(user_message) > 2000:
        return jsonify({"error": "Message too long (max 2000 characters)"}), 400

    # Get or initialize session history
    if "chat_history" not in session:
        session["chat_history"] = []

    conversation_history = session["chat_history"]

    # Generate AI response
    result = generate_response(user_message, conversation_history)
    response_text = result["text"]

    # Convert markdown to HTML for frontend rendering
    html_response = markdown.markdown(
        response_text,
        extensions=["tables", "fenced_code", "nl2br"],
    )

    # Update session history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": response_text})

    # Keep history at max 20 messages (10 turns)
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    session["chat_history"] = conversation_history
    session.modified = True

    return jsonify({
        "response": response_text,
        "html_response": html_response,
        "meta": {
            "model": result["model"],
            "mode": result["mode"],
            "tokens": result["tokens_used"],
            "timestamp": datetime.now().strftime("%H:%M"),
        },
    })


@app.route("/api/chat/clear", methods=["POST"])
def api_clear_chat():
    """Clear the conversation history for the current session."""
    session.pop("chat_history", None)
    return jsonify({"status": "cleared"})


@app.route("/api/weather/<location>")
def api_weather(location):
    """Get weather data for a location."""
    data = get_weather_data(location)
    return jsonify(data)


@app.route("/api/market")
def api_market():
    """Get current market prices."""
    crop = request.args.get("crop")
    state = request.args.get("state")
    data = get_market_prices(crop=crop, state=state)
    return jsonify(data)


@app.route("/api/schemes")
def api_schemes():
    """Get government schemes."""
    category = request.args.get("category")
    data = get_government_schemes(category=category)
    return jsonify(data)


@app.route("/api/crop-recommendation")
def api_crop():
    """Get crop recommendation."""
    soil = request.args.get("soil", "alluvial")
    season = request.args.get("season", "kharif")
    state = request.args.get("state", "Maharashtra")
    data = get_crop_recommendation(soil, season, state)
    return jsonify(data)


@app.route("/api/status")
def api_status():
    """Health check and configuration status."""
    has_api_key = bool(IBM_API_KEY)
    has_project_id = bool(WATSONX_PROJECT_ID)
    return jsonify({
        "status": "running",
        "agent": AGENT_NAME,
        "model": GRANITE_MODEL_ID,
        "watsonx_configured": has_api_key and has_project_id,
        "mode": "watsonx" if (has_api_key and has_project_id) else "demo",
        "timestamp": datetime.now().isoformat(),
    })


# ─────────────────────────────────────────────────────────────────
#  Error Handlers
# ─────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print(f"\n{'='*60}")
    print(f"  {AGENT_NAME}")
    print(f"  IBM watsonx.ai Smart Farming Advisor")
    print(f"{'='*60}")
    print(f"  Mode   : {'watsonx.ai (IBM Granite)' if IBM_API_KEY else 'DEMO (no credentials)'}")
    print(f"  Model  : {GRANITE_MODEL_ID}")
    print(f"  Port   : {port}")
    print(f"  Debug  : {debug}")
    print(f"  URL    : http://localhost:{port}")
    print(f"{'='*60}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
