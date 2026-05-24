# 🌍 AI City Intelligence Agent

**Premium AI-powered dashboard** for real-time weather, live news, and travel safety intelligence — built with Streamlit + LangChain + Groq.

A portfolio-quality SaaS-style experience that combines live APIs with an intelligent agent to deliver structured, beautiful, and actionable insights.

---

## ✨ Features

### 🧠 Intelligent Agent
- Powered by **LangChain** + **Groq** (`llama-3.3-70b-versatile`)
- Automatically decides when to use Weather Tool, News Tool, or both
- Handles complex queries like *"Is Bangalore safe for travel today?"*

### 🌡️ Weather Intelligence
- Beautiful KPI cards instead of raw text
- Shows: Temperature, Feels Like, Humidity, Wind Speed, Pressure, Visibility, Condition
- Clean 6-column responsive layout

### 📰 Live News Dashboard
- Each news item rendered as a premium card
- **Full clickable URLs** (no hidden links)
- Source badges + numbering
- Up to 6 latest relevant headlines

### 🛡️ Travel Safety Analysis
- Combines weather + news for safety queries
- Smart verdict badges:
  - ✅ **SAFE FOR TRAVEL**
  - ⚠️ **CAUTION ADVISED**
  - ⛔ **AVOID / HIGH RISK**
- Clear explanation + practical advice

### 🔧 Agent Transparency
- Live tool execution tracker
- Shows exactly which tools were called
- Full visibility into agent reasoning

### 🎨 Premium UI/UX
- Modern dark SaaS theme with gradients
- Responsive dashboard layout
- Clean chat + persistent intelligence panel
- Sidebar with API health indicators, example queries, and clickable history
- Beautiful empty states and loading experience

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-city-intelligence-agent.git
cd ai-city-intelligence-agent
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> **Get your free API keys:**
> - [Groq](https://console.groq.com/keys) (very fast + generous free tier)
> - [OpenWeather](https://openweathermap.org/api)
> - [Tavily](https://tavily.com) (AI search API)

### 4. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

We follow a **strict flat architecture** (no src/, components/, or nested folders):

```
AI_City_Intelligence_Agent/
├── app.py              # Main Streamlit dashboard + UI
├── agent.py            # LangChain agent creation + system prompt
├── tools.py            # Weather + News tools (structured JSON output)
├── config.py           # Environment validation
├── requirements.txt    # All dependencies
├── .env                # Your API keys (gitignored)
└── .gitignore
```

> **Important**: This structure is intentional. The app must always run with `streamlit run app.py`.

---

## 🛠️ Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| Frontend           | Streamlit (custom dark theme + HTML) |
| Agent Framework    | LangChain 0.2 + Tool Calling Agent  |
| LLM                | Groq (Llama-3.3-70B)                |
| News Search        | Tavily Search API                   |
| Weather            | OpenWeatherMap API                  |
| Language           | Python 3.10+                        |

---

## 💬 Example Queries

Try these in the app:

- `Weather in Mumbai`
- `Current news in Gwalior`
- `Is Bangalore safe for travel today?`
- `Weather and news in Delhi`
- `Latest AI news in India`
- `Hyderabad weather right now`

---

## 🖼️ Screenshots

> **Add your own screenshots here** (recommended for GitHub)

- Hero header + sidebar
- Weather KPI cards
- News cards with full URLs
- Travel safety verdict panel
- Agent transparency expander

---

## 📌 Key Design Decisions

- **No architecture changes** — only UI/UX improvements
- Tools return **structured JSON** for rich rendering (still compatible with LangChain agent)
- Full LLM answers are always shown (never truncated in final output)
- Dashboard state is always fresh after every query
- Everything runs from a single `app.py` entry point

---

## 🔒 Security

- All API keys are loaded from `.env`
- `.env` and `config.py` (in some setups) are gitignored
- No data is stored or logged externally

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss major changes.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) for extremely fast inference
- [LangChain](https://langchain.com) for the agent framework
- [Tavily](https://tavily.com) for high-quality search
- [Streamlit](https://streamlit.io) for rapid beautiful UIs

---


If you found this project useful, consider giving it a ⭐ on GitHub!
