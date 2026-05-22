# ============================================================
# 🌍 ENTERPRISE GENAI TRAVEL PLANNER UI
# ============================================================
# FILE: testui.py
# ============================================================

import streamlit as st
import requests
import time

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise GenAI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM LIGHT ELEGANT CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

/* ============================================================
GLOBAL
============================================================ */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #f8f7f4 !important;
    color: #1a1a2e !important;
}

/* ============================================================
MAIN APP — Pearl Gradient Background
============================================================ */

.stApp {
    background: linear-gradient(
        145deg,
        #f8f7f4 0%,
        #f0eef8 45%,
        #e9f4f0 100%
    ) !important;
}

/* ============================================================
SIDEBAR — Frosted Glass Light
============================================================ */

section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.82) !important;
    border-right: 1px solid rgba(124, 106, 247, 0.12) !important;
    backdrop-filter: blur(24px) !important;
    box-shadow: 4px 0 24px rgba(124, 106, 247, 0.06) !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #2d2b55 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ============================================================
SLIDER
============================================================ */

.stSlider > div > div > div {
    background: linear-gradient(90deg, #7c6af7, #06b6d4) !important;
}

.stSlider > div > div > div > div {
    background: #7c6af7 !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 8px rgba(124, 106, 247, 0.3) !important;
}

/* ============================================================
SELECTBOX / MULTISELECT / TEXT INPUT
============================================================ */

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid rgba(124, 106, 247, 0.18) !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid rgba(124, 106, 247, 0.18) !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 3px rgba(124, 106, 247, 0.10) !important;
}

/* ============================================================
TOGGLE
============================================================ */

.stToggle > label > div[data-checked="true"] {
    background-color: #7c6af7 !important;
}

/* ============================================================
BUTTON
============================================================ */

.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #7c6af7 0%, #5b4fcf 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.3px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 20px rgba(124, 106, 247, 0.25) !important;
    margin-top: 6px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(124, 106, 247, 0.38) !important;
    background: linear-gradient(135deg, #8f7ff9 0%, #6b5fd4 100%) !important;
}

/* ============================================================
CHAT INPUT
============================================================ */

.stChatInput > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1.5px solid rgba(124, 106, 247, 0.20) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(124, 106, 247, 0.07) !important;
}

.stChatInput > div:focus-within {
    border-color: #7c6af7 !important;
    box-shadow: 0 4px 24px rgba(124, 106, 247, 0.16) !important;
}

.stChatInput textarea {
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

.stChatInput button {
    background: #7c6af7 !important;
    border-radius: 10px !important;
}

/* ============================================================
CHAT MESSAGES
============================================================ */

[data-testid="stChatMessageContent"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    color: #2d2b55 !important;
}

/* ============================================================
SPINNER / STATUS
============================================================ */

.stSpinner > div {
    border-top-color: #7c6af7 !important;
}

.stStatus {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(124, 106, 247, 0.14) !important;
    border-radius: 12px !important;
    color: #2d2b55 !important;
}

/* ============================================================
MARKDOWN IN MAIN AREA
============================================================ */

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Playfair Display', serif !important;
    color: #1a1a2e !important;
}

.stMarkdown p, .stMarkdown li {
    color: #3d3b5c !important;
    font-family: 'DM Sans', sans-serif !important;
    line-height: 1.75 !important;
}

.stMarkdown strong {
    color: #1a1a2e !important;
}

.stMarkdown code {
    background: rgba(124, 106, 247, 0.08) !important;
    color: #5b4fcf !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ============================================================
CUSTOM CARDS
============================================================ */

.chat-container {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(124, 106, 247, 0.10);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(18px);
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(124, 106, 247, 0.06);
}

.user-message {
    background: linear-gradient(135deg, #7c6af7, #5b4fcf);
    padding: 16px 20px;
    border-radius: 18px 18px 4px 18px;
    margin: 16px 0 16px 25%;
    color: white;
    font-size: 14px;
    line-height: 1.65;
    font-family: 'DM Sans', sans-serif;
    box-shadow: 0 6px 20px rgba(124, 106, 247, 0.22);
}

.ai-message {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(124, 106, 247, 0.11);
    padding: 22px 26px;
    border-radius: 4px 18px 18px 18px;
    margin: 16px 25% 16px 0;
    font-size: 14px;
    line-height: 1.75;
    font-family: 'DM Sans', sans-serif;
    color: #2d2b55;
    backdrop-filter: blur(16px);
    box-shadow: 0 6px 24px rgba(124, 106, 247, 0.07);
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 38px;
    font-weight: 500;
    color: #1a1a2e;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}

.title-accent {
    background: linear-gradient(90deg, #7c6af7, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #7c7a9e;
    font-size: 15px;
    margin-bottom: 28px;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.2px;
}

.metric-card {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(124, 106, 247, 0.11);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 16px rgba(124, 106, 247, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(124, 106, 247, 0.11);
}

.metric-num {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 500;
    color: #7c6af7;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 12px;
    color: #9a98bb;
    font-weight: 500;
    letter-spacing: 0.3px;
}

.status-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.4px;
    margin-right: 6px;
    font-family: 'DM Sans', sans-serif;
}

.pill-purple { background: rgba(124,106,247,0.10); color: #7c6af7; border: 1px solid rgba(124,106,247,0.18); }
.pill-teal   { background: rgba(6,182,212,0.10);   color: #0891b2; border: 1px solid rgba(6,182,212,0.18); }
.pill-green  { background: rgba(16,185,129,0.10);  color: #059669; border: 1px solid rgba(16,185,129,0.18); }

/* ============================================================
SCROLLBAR
============================================================ */

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,106,247,0.18); border-radius: 10px; }

/* ============================================================
HIDE STREAMLIT BRANDING
============================================================ */

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-title">
    🌍 Enterprise <span class="title-accent">GenAI</span> Travel Planner
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
    Multi-Agent AI Powered Global Travel Intelligence Platform &nbsp;
    <span class="status-pill pill-purple">✦ Open AI</span>
    <span class="status-pill pill-teal">⊕ Google Places</span>
    <span class="status-pill pill-green">● Live</span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR  (your original logic, unchanged)
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ AI Travel Control Center")

    # use_current_location = st.checkbox(
    #     "📍 Use Current Location"
    # )

    from_location = st.text_input(
        "From Location",
        placeholder="Chennai, India"
    )

    destination = st.text_input(
        "Destination",
        placeholder="Tokyo, Japan"
    )

    budget = st.slider(
        "💰 Budget (₹)",
        5000,
        1000000,
        100000,
        step=5000
    )

    days = st.slider(
        "📅 Number of Days",
        1,
        30,
        5
    )

    travel_style = st.selectbox(
        "✨ Travel Style",
        [
            "Luxury",
            "Budget",
            "Solo",
            "Family",
            "Adventure",
            "Corporate",
            "Romantic"
        ]
    )

    food_preference = st.multiselect(
        "🍜 Food Preference",
        [
            "Veg",
            "Non-Veg",
            "Vegan",
            "Jain",
            "Halal",
            "Gluten-Free"
        ]
    )

    transport_mode = st.selectbox(
        "🚕 Transport",
        [
            "Flight",
            "Train",
            "Cab",
            "Metro",
            "Walk",
            "Bike"
        ]
    )

    hotel_type = st.select_slider(
        "🏨 Hotel Preference",
        options=[
            "3 Star",
            "4 Star",
            "5 Star",
            "Resort",
            "Villa"
        ]
    )

    ai_mode = st.selectbox(
        "🧠 AI Planning Mode",
        [
            "Smart Saver",
            "Luxury",
            "Explorer",
            "Productivity"
        ]
    )

    weather_aware = st.toggle(
        "🌦 Weather-Aware Planning",
        value=True
    )

    optimize_budget = st.toggle(
        "💸 Budget Optimization",
        value=True
    )

# ============================================================
# CHAT EXPERIENCE  (your original logic, only response key fixed)
# ============================================================

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

user_query = st.chat_input(
    "Ask AI anything about your trip..."
)

if user_query:

    st.markdown(f"""
    <div class="user-message">
    {user_query}
    </div>
    """, unsafe_allow_html=True)

    payload = {
        "destination":    destination,
        "budget":         budget,
        "days":           days,
        "travel_style":   travel_style,
        "food_preference": ",".join(food_preference),
        "transport_mode": transport_mode
    }

    with st.spinner("🤖 AI Agents Planning Your Journey..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/generate-itinerary",
                json=payload,
                timeout=300
            )

            data = response.json()

            if response.status_code == 200:

                # ------------------------------------------------
                # FIX: your backend wraps in {"status","result"}
                # so itinerary is at data["result"]["itinerary"]
                # ------------------------------------------------
                itinerary = (
                    data.get("result", {}).get("itinerary")
                    or data.get("itinerary")
                    or "No itinerary generated."
                )

                time.sleep(1)

                st.markdown(f"""
                <div class="ai-message">
                {itinerary}
                </div>
                """, unsafe_allow_html=True)

            else:

                st.error(f"Backend Error: {response.text}")

        except requests.exceptions.ConnectionError:

            st.error(
                "⚠️ Cannot connect to backend. "
                "Start it first:  uvicorn main:app --reload --port 8000"
            )

        except Exception as e:

            st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ANALYTICS SECTION  (your original layout, updated styling)
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-num">150+</div>
        <div class="metric-label">Countries Supported</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-num">AI Powered</div>
        <div class="metric-label">Multi-Agent System</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-num">Open AI</div>
        <div class="metric-label">Enterprise Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-num">Real-Time</div>
        <div class="metric-label">Travel Optimization</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER  (unchanged)
# ============================================================

st.markdown("""
<br>
<center style="color:#9a98bb; font-size:12px; font-family:'DM Sans',sans-serif; letter-spacing:0.3px;">
    AI-Native Enterprise Travel Intelligence Platform<br>
    Built with FastAPI &nbsp;·&nbsp; Open AI &nbsp;·&nbsp; Google Places &nbsp;·&nbsp; Streamlit
</center>
""", unsafe_allow_html=True)
