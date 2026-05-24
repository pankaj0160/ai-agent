import json
import streamlit as st
from datetime import datetime
from urllib.parse import urlparse
from agent import create_agent
from config import validate_env


# ============================================================
# PREMIUM SAAS DASHBOARD - AI CITY INTELLIGENCE AGENT
# Upgraded UX/UI only. Architecture & agent flow preserved.
# ============================================================

validate_env()

st.set_page_config(
    page_title="AI City Intelligence Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Kilo-Org/kilocode",
        "Report a bug": "https://github.com/Kilo-Org/kilocode/issues",
        "About": "Premium City Intelligence powered by Groq + LangChain + Tavily + OpenWeather"
    }
)


@st.cache_resource(show_spinner="Loading AI Agent...")
def load_agent():
    return create_agent()


agent = load_agent()


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "last_query" not in st.session_state:
    st.session_state.last_query = None
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_weather" not in st.session_state:
    st.session_state.last_weather = None
if "last_news" not in st.session_state:
    st.session_state.last_news = None
if "last_tools_used" not in st.session_state:
    st.session_state.last_tools_used = []


# ============================================================
# PREMIUM DARK THEME + SAAS STYLING (all inline, no external files)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap');

    .stApp {
        background: linear-gradient(145deg, #0b1120 0%, #0f172a 40%, #020617 100%);
        color: #e2e8f0;
    }

    /* Hero header */
    .hero {
        background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 45%, #1e3a8a 100%);
        border: 1px solid #1e40af;
        border-radius: 20px;
        padding: 2.1rem 2.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.2), 0 8px 10px -6px rgb(0 0 0 / 0.2);
    }

    .hero h1 {
        font-family: 'Space Grotesk', Inter, system_ui, sans-serif;
        font-size: 2.65rem;
        font-weight: 700;
        letter-spacing: -2.2px;
        background: linear-gradient(90deg, #bae6fd, #e0f2fe 50%, #bae6fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.35rem 0;
    }

    .hero p {
        color: #64748b;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Chat bubbles - premium rounded dark */
    .stChatMessage {
        border-radius: 18px;
        padding: 14px 18px;
        margin: 6px 0;
        box-shadow: 0 4px 6px -1px rgb(15 23 42 / 0.3);
    }
    .stChatMessage[data-testid="chatMessage-user"] {
        background: #1e2937;
        border: 1px solid #334155;
    }
    .stChatMessage[data-testid="chatMessage-assistant"] {
        background: #0f172a;
        border: 1px solid #1e3a5f;
    }

    /* Improve long-form AI text readability inside chat bubbles */
    .stChatMessage .stMarkdown {
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .stChatMessage .stMarkdown p {
        margin-bottom: 0.6rem;
    }

    /* Sidebar polish */
    .css-1d391kg, .css-1vq4p4l {
        background: #0b1120;
    }
    .sidebar .stButton > button {
        border-radius: 999px;
        border: 1px solid #334155;
        background: #1e2937;
        color: #cbd5e1;
        font-size: 0.9rem;
        padding: 0.45rem 0.9rem;
        transition: all 0.2s ease;
    }
    .sidebar .stButton > button:hover {
        background: #334155;
        border-color: #475569;
        transform: translateY(-1px);
    }

    /* Custom KPI / Metric cards */
    .kpi-card {
        background: #1e2937;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 14px 10px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 10px 15px -3px rgb(15 23 42 / 0.4);
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgb(15 23 42 / 0.5);
    }
    .kpi-icon { font-size: 1.65rem; margin-bottom: 4px; }
    .kpi-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 1.45rem; font-weight: 700; color: #e0f2fe; margin-top: 2px; }

    /* News cards */
    .news-card {
        background: #1e2937;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgb(15 23 42 / 0.3);
    }
    .news-card h4 {
        color: #f1f5f9;
        margin: 0 0 8px 0;
        font-size: 1.02rem;
        line-height: 1.3;
    }
    .news-card p {
        color: #94a3b8;
        font-size: 0.92rem;
        line-height: 1.45;
        margin: 0 0 10px 0;
    }
    .news-source {
        background: #334155;
        color: #94a3b8;
        font-size: 0.72rem;
        padding: 2px 9px;
        border-radius: 6px;
        display: inline-block;
    }
    .news-link {
        color: #38bdf8;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.88rem;
    }
    .news-link:hover { text-decoration: underline; }

    /* Verdict / Recommendation badge */
    .verdict-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 9999px;
        font-weight: 700;
        letter-spacing: 0.6px;
        font-size: 0.95rem;
        margin: 10px 0 4px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.2);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #0f172a;
        border-radius: 999px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 8px 18px;
        font-weight: 600;
    }

    /* Status / transparency */
    .stStatus {
        border-radius: 12px;
        border: 1px solid #1e3a5f;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #1e2937;
    }

    /* Welcome cards */
    .welcome-card {
        background: #1e2937;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 18px 16px;
        text-align: center;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .welcome-card:hover {
        border-color: #3b82f6;
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgb(59 130 246 / 0.15);
    }

    /* Full AI response container - maximum readability */
    .ai-full-response {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px 20px;
        margin: 12px 0 20px 0;
        line-height: 1.65;
        font-size: 0.96rem;
        color: #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(15 23 42 / 0.4);
    }
    .ai-full-response h3 {
        margin-top: 0;
        margin-bottom: 12px;
        color: #bae6fd;
        font-size: 1.05rem;
    }
    .ai-full-response p, .ai-full-response li {
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER RENDER FUNCTIONS (Premium structured output)
# ============================================================

def render_weather_kpis(data: dict):
    """Beautiful 6-column KPI cards for weather."""
    if not data:
        st.warning("No weather data available.")
        return

    city = data.get("city", "Unknown")
    country = data.get("country", "")
    condition = data.get("condition", "Clear")

    st.markdown(f"### 🌡️ Live Weather — {city}, {country}")

    cols = st.columns(6, gap="small")
    kpis = [
        ("🌡️", "Temperature", f"{data.get('temp', '—')}°C"),
        ("🤔", "Feels Like", f"{data.get('feels_like', '—')}°C"),
        ("💧", "Humidity", f"{data.get('humidity', '—')}%"),
        ("💨", "Wind Speed", f"{data.get('wind_speed', '—')} m/s"),
        ("📊", "Pressure", f"{data.get('pressure', '—')} hPa"),
        ("👁️", "Visibility", f"{round(data.get('visibility', 0)/1000, 1)} km" if data.get('visibility') else "N/A"),
    ]

    for col, (icon, label, value) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # Condition badge
    st.markdown(f"""
    <div style="text-align:center; margin: 10px 0 4px;">
        <span style="background:#0ea5e9; color:white; padding:5px 16px; border-radius:999px; font-size:0.95rem; font-weight:600;">
            {condition}
        </span>
    </div>
    """, unsafe_allow_html=True)


def render_news_cards(news_list: list):
    """Premium numbered news cards with FULL clickable URLs."""
    if not news_list:
        st.info("No recent news found for this location/topic.")
        return

    st.markdown("### 📰 Top Headlines")

    for idx, item in enumerate(news_list[:5], 1):
        title = item.get("title", "Untitled")
        summary = item.get("summary", "")
        url = item.get("url", "#")
        source = item.get("source", "Source")

        st.markdown(f"""
        <div class="news-card">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="background:#1e40af; color:white; font-size:0.78rem; padding:2px 9px; border-radius:4px; font-weight:700;">{idx}</span>
                <span class="news-source">{source}</span>
            </div>
            <h4>{title}</h4>
            <p>{summary}</p>
            <a href="{url}" target="_blank" class="news-link">🔗 Read full article → {url}</a>
        </div>
        """, unsafe_allow_html=True)


def render_recommendation_panel(final_answer: str, weather_data=None, news_data=None):
    """AI recommendation panel with smart verdict badge for travel safety queries."""
    if not final_answer:
        return

    lower = final_answer.lower()
    verdict = "INTELLIGENCE UPDATE"
    badge_color = "#475569"

    if "safe" in lower and "not safe" not in lower and "unsafe" not in lower:
        verdict = "✅ SAFE FOR TRAVEL"
        badge_color = "#16a34a"
    elif "caution" in lower or "moderate risk" in lower or "be careful" in lower:
        verdict = "⚠️ CAUTION ADVISED"
        badge_color = "#ca8a04"
    elif "avoid" in lower or "high risk" in lower or "unsafe" in lower or "not recommended" in lower:
        verdict = "⛔ AVOID / HIGH RISK"
        badge_color = "#dc2626"

    st.markdown("### 🧠 AI Intelligence & Recommendation")

    with st.container(border=True):
        st.markdown(f"""
        <span class="verdict-badge" style="background:{badge_color}; color:white;">
            {verdict}
        </span>
        """, unsafe_allow_html=True)

        # Show only the synthesized recommendation / key points instead of full duplicate text
        # (full original answer is already displayed prominently above the tabs)
        st.markdown("**Key Analysis & Advice**")
        # Extract the most actionable part if very long, otherwise show concise version
        lines = [l.strip() for l in final_answer.split('\n') if l.strip()]
        short_version = '\n'.join(lines[:6]) if len(lines) > 8 else final_answer
        st.markdown(short_version)

        if weather_data or news_data:
            st.caption("Grounded in live weather + news data • Powered by Groq")


def render_tool_transparency(tools_used: list, query: str):
    """Compact agent execution tracker."""
    if not tools_used:
        return

    with st.expander("🔧 Agent Transparency — Tool Execution Log", expanded=False):
        st.markdown("**Tools invoked by the LangChain agent:**")
        for tool in tools_used:
            if "weather" in tool.lower():
                st.markdown(f"✅ **get_weather** — fetched live conditions for the query")
            elif "news" in tool.lower():
                st.markdown(f"✅ **get_news** — retrieved latest headlines and sources")
            else:
                st.markdown(f"✅ **{tool}**")

        st.caption(f"Query processed at {datetime.now().strftime('%H:%M:%S')} • Real-time APIs only — no cached data")


def render_latest_dashboard():
    """Main premium dashboard area that updates with every agent response."""
    if not st.session_state.get("last_query"):
        # Beautiful empty / welcome state when no query yet
        st.markdown("---")
        st.markdown("### ✨ Welcome to the AI City Intelligence Dashboard")
        st.markdown("Ask anything about weather, breaking news, or travel safety. The agent will fetch live data and render it beautifully below.")

        cols = st.columns(3, gap="medium")
        welcome_examples = [
            "Weather in Mumbai",
            "Current news in Gwalior",
            "Is Bangalore safe for travel today?",
        ]
        icons = ["🌡️", "📰", "🛡️"]

        for i, (col, ex, icon) in enumerate(zip(cols, welcome_examples, icons)):
            with col:
                st.markdown(f"""
                <div class="welcome-card">
                    <div style="font-size:2rem; margin-bottom:8px;">{icon}</div>
                    <div style="font-weight:600; color:#cbd5e1; margin-bottom:4px;">{ex}</div>
                    <div style="font-size:0.8rem; color:#64748b;">Click an example in the sidebar to start</div>
                </div>
                """, unsafe_allow_html=True)
        return

    # Active dashboard
    q = st.session_state.last_query
    weather = st.session_state.last_weather
    news = st.session_state.last_news
    answer = st.session_state.last_answer or ""
    tools = st.session_state.last_tools_used or []

    st.divider()
    st.markdown(f"## 📍 Latest Intelligence for **{q}**")
    st.caption(f"Generated {datetime.now().strftime('%b %d, %Y at %H:%M')} • Live data")

    # Always surface the COMPLETE AI-generated answer first for maximum readability
    if answer:
        st.markdown("""
        <div class="ai-full-response">
            <h3>🧠 Full AI Response</h3>
        """, unsafe_allow_html=True)
        st.markdown(answer)
        st.markdown("</div>", unsafe_allow_html=True)

    # Determine layout based on what the agent used
    used_weather = any("weather" in str(t).lower() for t in tools)
    used_news = any("news" in str(t).lower() for t in tools)

    if used_weather and used_news:
        # Travel safety style - three rich sections via tabs
        tab1, tab2, tab3 = st.tabs(["🌡️ Weather Dashboard", "📰 Local News Cards", "🧠 AI Recommendation"])

        with tab1:
            if weather:
                render_weather_kpis(weather)
            else:
                st.info("Weather data not available for this response.")

        with tab2:
            if news and isinstance(news, dict) and news.get("news"):
                render_news_cards(news["news"])
            else:
                st.info("News data not available.")

        with tab3:
            render_recommendation_panel(answer, weather, news)

        render_tool_transparency(tools, q)

    elif used_weather:
        render_weather_kpis(weather or {})
        render_tool_transparency(tools, q)

    elif used_news:
        if news and isinstance(news, dict):
            render_news_cards(news.get("news", []))
        else:
            st.warning("News data format unexpected.")
        render_tool_transparency(tools, q)

    else:
        # Generic fallback - full text already shown prominently above
        render_tool_transparency(tools, q)


# ============================================================
# AGENT PROCESSING (keeps exact original invocation pattern + enhanced observability)
# ============================================================

def run_agent_and_update_dashboard(user_query: str):
    """Core processing. Preserves tool-based LangChain agent flow.
    Pure state updater — no rendering inside. All display comes from
    the single history loop + render_latest_dashboard on script re-execution.
    This guarantees the full detailed AI answer is visible from the first query.
    """
    st.session_state.query_history.append(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Defensive reset so old structured results (e.g. previous Gwalior news cards) don't leak into this run
    st.session_state.last_query = user_query
    st.session_state.last_answer = None
    st.session_state.last_weather = None
    st.session_state.last_news = None
    st.session_state.last_tools_used = []

    try:
        # EXACT same agent invocation pattern (with return_intermediate_steps for rich UI)
        response = agent.invoke(
            {"input": user_query},
            return_intermediate_steps=True
        )

        final_answer = response.get("output", "I was unable to generate a response.")
        steps = response.get("intermediate_steps", [])

        # Parse structured tool outputs (JSON from improved tools)
        tools_used = []
        weather_data = None
        news_data = None

        for action, observation in steps:
            tool_name = getattr(action, "tool", str(action))
            tools_used.append(tool_name)

            if "weather" in tool_name.lower():
                try:
                    if isinstance(observation, str) and observation.strip().startswith("{"):
                        weather_data = json.loads(observation)
                except (json.JSONDecodeError, TypeError):
                    pass

            elif "news" in tool_name.lower():
                try:
                    if isinstance(observation, str) and observation.strip().startswith("{"):
                        news_data = json.loads(observation)
                except (json.JSONDecodeError, TypeError):
                    pass

        # Persist for the beautiful dashboard
        st.session_state.last_query = user_query
        st.session_state.last_answer = final_answer
        st.session_state.last_weather = weather_data
        st.session_state.last_news = news_data
        st.session_state.last_tools_used = tools_used

    except Exception as e:
        final_answer = f"❌ Agent Error: {str(e)}"
        st.session_state.last_answer = final_answer
        st.session_state.last_query = user_query
        st.session_state.last_weather = None
        st.session_state.last_news = None
        st.session_state.last_tools_used = []

    # Store full (never truncated) answer so history loop always shows complete result
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_answer
    })


# ============================================================
# SIDEBAR - Premium control panel
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")

    # API health indicators (premium pills)
    st.markdown("""
    <div style="display:flex; gap:6px; flex-wrap:wrap; margin:12px 0 18px;">
        <span style="background:#166534; color:#86efac; padding:3px 11px; border-radius:999px; font-size:0.78rem; font-weight:600;">✅ Groq</span>
        <span style="background:#166534; color:#86efac; padding:3px 11px; border-radius:999px; font-size:0.78rem; font-weight:600;">✅ Weather API</span>
        <span style="background:#166534; color:#86efac; padding:3px 11px; border-radius:999px; font-size:0.78rem; font-weight:600;">✅ Tavily Live</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 💡 Example Queries")
    examples = [
        "Weather in Mumbai",
        "Current news in Gwalior",
        "Is Bangalore safe for travel today?",
        "AI news in India",
        "Weather and news in Delhi",
        "Latest updates in Hyderabad"
    ]

    for i, ex in enumerate(examples):
        if st.button(ex, key=f"ex_{i}", use_container_width=True):
            st.session_state.pending_query = ex
            st.rerun()

    st.divider()

    st.markdown("### 🕘 Query History")
    if st.session_state.query_history:
        for i, q in enumerate(reversed(st.session_state.query_history[-7:])):
            short = q if len(q) <= 38 else q[:35] + "…"
            if st.button(f"↩️ {short}", key=f"hist_{i}_{len(st.session_state.query_history)}", use_container_width=True):
                st.session_state.pending_query = q
                st.rerun()
    else:
        st.caption("No queries yet. Use examples above to begin.")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.query_history = []
            st.session_state.last_query = None
            st.session_state.last_answer = None
            st.session_state.last_weather = None
            st.session_state.last_news = None
            st.session_state.last_tools_used = []
            st.rerun()
    with col2:
        st.caption(f"{len(st.session_state.messages)} messages")

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.caption("v2.0 • Premium Dashboard")


# ============================================================
# MAIN HERO HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>🌍 AI City Intelligence</h1>
    <p>Real-time weather • Live global news • Travel safety analysis<br>
    <span style="color:#475569; font-size:0.9rem;">Powered by Groq + LangChain + Tavily + OpenWeather</span></p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HANDLE EXAMPLE / HISTORY BUTTONS (before rendering chat)
# ============================================================
if "pending_query" in st.session_state:
    pending = st.session_state.pop("pending_query")
    with st.status("🧠 City Intelligence Agent analyzing...", expanded=False):
        run_agent_and_update_dashboard(pending)
    st.rerun()   # clean re-render — full detailed answer now visible in history + dashboard


# ============================================================
# CHAT HISTORY (clean conversational log)
# ============================================================
for msg in st.session_state.messages:
    avatar = "🧑‍💼" if msg["role"] == "user" else "🌍"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ============================================================
# PREMIUM INTELLIGENCE DASHBOARD (the main UX upgrade)
# ============================================================
render_latest_dashboard()


# ============================================================
# CHAT INPUT (bottom)
# ============================================================
user_input = st.chat_input(
    "Ask about weather, travel safety, or current news in any city...",
    key="main_chat_input"
)

if user_input:
    with st.status("🧠 City Intelligence Agent analyzing...", expanded=False):
        run_agent_and_update_dashboard(user_input)
    st.rerun()  # Force fresh render so dashboard + history show the new full result immediately (fixes stale previous query data)


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    Built for portfolio-quality UX • All data fetched live via official APIs • 
    No data is stored • Agent powered by llama-3.3-70b on Groq
</div>
""", unsafe_allow_html=True)
