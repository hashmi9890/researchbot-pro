import streamlit as st
import os
from dotenv import load_dotenv

# 1. PAGE CONFIGURATION (Must be at the very top)
st.set_page_config(
    page_title="StrategyAI Pro",
    page_icon="🎯",
    layout="wide"
)

# 2. PREMIUM CSS INJECTION
st.markdown("""
<style>
    /* Executive Dark Theme */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f0c29);
        color: #F9FAFB;
    }
    
    /* Hero Section */
    .hero-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 4rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 3rem;
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(to right, #6366F1, #A855F7, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    /* Cards */
    .agent-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        border-color: #6366F1;
        transform: translateY(-5px);
        background: rgba(99, 102, 241, 0.05);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. UI LAYOUT
st.markdown("""
<div class="hero-box">
    <h1 class="hero-title">StrategyAI Pro</h1>
    <p style='font-size: 1.2rem; color: #9CA3AF;'>The Future of Executive Decision Making</p>
</div>
""", unsafe_allow_html=True)

# 4. SIDEBAR SETUP
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("Control Center")
    st.divider()
    model = st.selectbox("LLM Model", ["Llama 3.3 70B", "Llama 3.1 8B"])
    temp = st.slider("Strategy Creativity", 0.1, 0.9, 0.3)
    st.divider()
    st.info("System Status: 🟢 Secure")

# 5. MAIN INTERFACE
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="agent-card">👔 <b>CEO Agent</b><br><small>Strategic Planning</small></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="agent-card">💰 <b>CFO Agent</b><br><small>Financial Analysis</small></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="agent-card">🎯 <b>Solver Agent</b><br><small>Problem Solving</small></div>', unsafe_allow_html=True)

st.write("")
st.header("Strategic Input")
user_input = st.text_area("Describe your business challenge:", placeholder="e.g. How to scale our SaaS to $5M ARR...")

if st.button("🚀 Generate Analysis"):
    with st.status("Deploying Executive Agents...", expanded=True) as status:
        st.write("👔 CEO is reviewing market trends...")
        # Yahan tumhara purana CrewAI logic aayega
        status.update(label="Analysis Complete!", state="complete", expanded=False)
    st.success("Strategy generated successfully!")