# 🌾 AgriSense AI — IBM Granite–Powered Smart Farming Advisor

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

A professional AI-powered smart farming web application built with **Python Flask** and **IBM watsonx.ai (IBM Granite foundation models)**. AgriSense AI provides personalized farming advice in English and 10 Indian regional languages.

## 🚀 Live Demo
https://agrisense-s8vb.onrender.com/

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Chat Advisor** | Conversational IBM Granite–powered farming expert |
| 🌾 **Crop Recommendations** | Season, soil & region-based crop suggestions |
| 🌤️ **Weather Advisory** | Farming-specific weather summaries & forecasts |
| 🐛 **Pest & Disease Management** | IPM guidance with biological & chemical controls |
| 📊 **Market Prices** | Mandi prices, MSP comparisons, trend indicators |
| 🏛️ **Government Schemes** | PM-KISAN, PMFBY, KCC and 50+ schemes explained |
| 🌍 **Multilingual** | English + Hindi, Tamil, Telugu, Kannada & 6 more |
| 🌙 **Dark / Light Mode** | Persistent theme toggle |
| 📱 **Mobile Responsive** | Full mobile-first design |

---

## 🏗️ Project Structure

```
AgriSense/
├── app.py                    # Flask app + watsonx.ai integration
├── agent_instructions.py     # 🔧 CUSTOMIZE AGENT HERE
├── requirements.txt
├── .env.example
├── .env                      # (create from .env.example — NOT committed)
│
├── tools/                    # Placeholder tool functions (ready for real APIs)
│   ├── __init__.py
│   ├── weather_tool.py       # Weather data (connect OpenWeatherMap)
│   ├── crop_tool.py          # Crop recommendations (connect ML model)
│   ├── market_tool.py        # Market prices (connect Agmarknet API)
│   ├── scheme_tool.py        # Government schemes database
│   ├── soil_tool.py          # Soil health information
│   └── pest_tool.py          # Pest & disease management
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base layout with navbar & footer
│   ├── index.html            # Homepage — Hero, Features, Stats
│   ├── chat.html             # AI Chat interface
│   ├── dashboard.html        # Farming dashboard
│   ├── weather.html          # Weather information
│   ├── market.html           # Market prices table
│   ├── schemes.html          # Government schemes cards
│   ├── 404.html
│   └── 500.html
│
└── static/
    ├── css/style.css         # Custom CSS (glassmorphism, animations)
    └── js/
        ├── main.js           # Theme toggle, counters, status check
        └── chat.js           # Chat interface logic
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/your-username/agrisense-ai.git
cd agrisense-ai

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example env file
copy .env.example .env        # Windows
cp .env.example .env          # macOS/Linux

# Edit .env with your credentials
notepad .env                  # Windows
nano .env                     # macOS/Linux
```

Fill in:
```env
IBM_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=your-long-random-secret-key
```

### 3. Run the Application

```bash
python app.py
```

Open your browser at **http://localhost:5000**

> **No IBM credentials?** The app runs in **Demo Mode** with pre-built responses. Add credentials later to connect IBM Granite.

---

## 🔑 Getting IBM Credentials

### IBM Cloud API Key
1. Go to [IBM Cloud IAM](https://cloud.ibm.com/iam/apikeys)
2. Click **Create an IBM Cloud API key**
3. Download or copy the key into `.env` as `IBM_API_KEY`

### watsonx.ai Project ID
1. Go to [IBM watsonx.ai](https://dataplatform.cloud.ibm.com)
2. Create a new project (or open existing)
3. Go to **Project Settings** → copy the **Project ID**
4. Paste into `.env` as `WATSONX_PROJECT_ID`

### Enable watsonx.ai Service
1. In your IBM Cloud account, provision **Watson Machine Learning** service
2. Associate it with your watsonx.ai project

---

## 🎛️ Customizing the AI Agent

Edit **`agent_instructions.py`** to change agent behavior:

```python
# Change the agent's name
AGENT_NAME = "MyFarmBot"

# Change tone and personality
AGENT_PERSONA = """You are a farming expert for Maharashtra farmers..."""

# Add or remove specialization areas
SPECIALIZATION_AREAS = """..."""

# Modify safety rules
SAFETY_RULES = """..."""

# Change response format
RESPONSE_FORMAT = """..."""
```

No changes to `app.py` needed — the `SYSTEM_PROMPT` is assembled automatically.

---

## 🔧 Connecting Real Data Sources

### Weather API
```python
# tools/weather_tool.py
import requests
import os

def get_weather_data(location: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }
    return requests.get(url, params=params).json()
```
Add `OPENWEATHER_API_KEY` to your `.env`.

### Market Prices (Agmarknet)
```python
# tools/market_tool.py — replace stub with:
url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
params = {"api-key": os.getenv("AGMARKNET_API_KEY"), "format": "json"}
```

---

## 🤖 Changing the IBM Granite Model

In `app.py`, update `GRANITE_MODEL_ID`:

```python
# Chat-optimized models (recommended)
GRANITE_MODEL_ID = "ibm/granite-13b-chat-v2"    # Default
GRANITE_MODEL_ID = "ibm/granite-7b-lab"          # Lighter & faster
GRANITE_MODEL_ID = "ibm/granite-20b-multilingual" # Multilingual

# See all models at: https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/chat` | POST | Send message, get AI response |
| `/api/chat/clear` | POST | Clear session chat history |
| `/api/status` | GET | Health check & config status |
| `/api/weather/<location>` | GET | Weather data for a location |
| `/api/market` | GET | Market prices (optional `?crop=Wheat`) |
| `/api/schemes` | GET | Government schemes list |
| `/api/crop-recommendation` | GET | Crop suggestions |

---

## 📦 Deployment

### Gunicorn (Production)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t agrisense-ai .
docker run -p 5000:5000 --env-file .env agrisense-ai
```

### IBM Code Engine / Cloud Foundry
```bash
# Ensure Procfile exists
echo "web: gunicorn app:app" > Procfile

# Deploy to IBM Cloud Foundry
ibmcloud cf push agrisense-ai --no-start
ibmcloud cf set-env agrisense-ai IBM_API_KEY your_key
ibmcloud cf set-env agrisense-ai WATSONX_PROJECT_ID your_project_id
ibmcloud cf start agrisense-ai
```

---

## 🔒 Security Notes

- **Never commit `.env`** — it contains your API keys
- `.env` is in `.gitignore` by default
- Use strong random value for `FLASK_SECRET_KEY` in production
- In production, set `FLASK_ENV=production`
- Consider rate limiting the `/api/chat` endpoint for public deployment

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- **IBM watsonx.ai** — Granite foundation models
- **ICAR** — Indian agricultural knowledge base
- **data.gov.in** — Open government data APIs
- **Bootstrap 5** — UI framework

---

*Made with ❤️ for Indian Farmers by AgriSense AI*
