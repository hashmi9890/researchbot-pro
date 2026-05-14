import streamlit as st
import os
from datetime import datetime

# ═══════════════════════════════════════════════
# 🔐 CONFIGURATION
# ═══════════════════════════════════════════════
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

st.set_page_config(
    page_title="StrategyAI Pro",
    page_icon="🎯",
    layout="wide"
)

# ═══════════════════════════════════════════════
# 🎨 CLAUDE-STYLE CSS
# ═══════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #0f0f0f; color: #ececec; }
    [data-testid="stSidebar"] { background: #1a1a1a; border-right: 1px solid #2d2d2d; }
    
    /* Input Area Styling */
    .stTextArea textarea {
        background: #1a1a1a;
        border: 1px solid #3d3d3d;
        border-radius: 12px;
        color: white;
        font-size: 16px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextArea textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
    }
    
    /* Chat Bubbles */
    .user-msg {
        background: #2d2d2d;
        border-radius: 12px 12px 0 12px;
        padding: 16px 20px;
        margin: 10px 0 10px auto;
        max-width: 85%;
        clear: both;
        float: right;
    }
    .ai-msg {
        background: #1e1e2e;
        border-left: 4px solid #4f46e5;
        border-radius: 0 12px 12px 12px;
        padding: 16px 20px;
        margin: 10px auto 10px 0;
        max-width: 90%;
        clear: both;
        float: left;
    }
    .clearfix::after { content: ""; clear: both; display: table; }
    
    /* Buttons */
    .stButton>button {
        background: #4f46e5; color: white; border: none;
        border-radius: 8px; padding: 12px 24px; font-weight: 600;
        transition: all 0.3s; width: 100%;
    }
    .stButton>button:hover { background: #6366f1; transform: translateY(-2px); }
    
    #MainMenu, footer, .stDeployButton { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# 🧠 SESSION STATE (Auto-Clear Logic)
# ═══════════════════════════════════════════════
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = "🎯 All Agents"

# ═══════════════════════════════════════════════
# 🎛️ SIDEBAR (Agent Selection)
# ═══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎯 Command Center")
    st.markdown("---")
    
    agents = [
        ("🎯 All Agents")]