import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

# ═══════════════════════════════════════════════
# 🔐 LOAD ENVIRONMENT (Local) or SECRETS (Cloud)
# ═══════════════════════════════════════════════
load_dotenv()

# Try Streamlit secrets first (for cloud), fallback to .env (local)
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    MODEL_NAME = st.secrets.get("MODEL_NAME", "groq/llama-3.3-70b-versatile")
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY or ""

# ═══════════════════════════════════════════════
# 🎨 PAGE CONFIGURATION
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="StrategyAI Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════
# 💎 PREMIUM CSS
# ═══════════════════════════════════════════════
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f0c29);
        color: #F9FAFB;
    }
    
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
    
    .agent-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        border-radius: 16px;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .agent-card:hover {
        border-color: #6366F1;
        transform: translateY(-5px);
        background: rgba(99, 102, 241, 0.05);
    }
    
    .result-box {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 2rem;
        border-radius: 16px;
        margin-top: 2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# 🎯 HERO SECTION
# ═══════════════════════════════════════════════
st.markdown("""
<div class="hero-box">
    <h1 class="hero-title">StrategyAI Pro</h1>
    <p style='font-size: 1.2rem; color: #9CA3AF; margin-top: 1rem;'>
        Executive Decisions, Powered by Multi-Agent AI
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# 🎛️ SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("Control Center")
    st.divider()
    
    model_choice = st.selectbox(
        "🤖 LLM Model",
        ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant", "groq/mixtral-8x7b-32768"]
    )
    
    temperature = st.slider("🎨 Creativity", 0.1, 0.9, 0.3, 0.1)
    
    st.divider()
    
    # Security Status
    if GROQ_API_KEY:
        st.success("🔐 API Key: Connected")
    else:
        st.error("❌ API Key: Missing")
    
    st.info("🟢 System: Operational")
    
    st.divider()
    st.caption("Built with ❤️ by Abdullah Hashmi")

# ═══════════════════════════════════════════════
# 🤖 AGENT CARDS
# ═══════════════════════════════════════════════
st.markdown("### 👥 Your Executive Team")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h2>👔</h2>
        <h3>CEO Agent</h3>
        <p style='color: #9CA3AF;'>Strategic Vision & Planning</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h2>💰</h2>
        <h3>CFO Agent</h3>
        <p style='color: #9CA3AF;'>Financial Analysis & ROI</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h2>🎯</h2>
        <h3>Problem Solver</h3>
        <p style='color: #9CA3AF;'>Creative Solutions</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════
# 💬 INPUT SECTION
# ═══════════════════════════════════════════════
st.markdown("### 📝 Strategic Input")

user_input = st.text_area(
    "Describe your business challenge:",
    placeholder="Example: How can we increase our SaaS revenue by 40% in Q2 without expanding the team?",
    height=120
)

col_a, col_b = st.columns([1, 4])
with col_a:
    analyze_btn = st.button("🚀 Generate Analysis", use_container_width=True, type="primary")

# ═══════════════════════════════════════════════
# 🧠 AI PROCESSING
# ═══════════════════════════════════════════════
if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️ Please describe your business challenge first.")
    elif not GROQ_API_KEY:
        st.error("❌ API Key not configured. Please contact admin.")
    else:
        with st.status("🚀 Deploying Executive Team...", expanded=True) as status:
            try:
                from langchain_groq import ChatGroq
                
                st.write("👔 CEO Agent analyzing strategy...")
                
                # Initialize LLM
                llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    temperature=temperature,
                    api_key=GROQ_API_KEY
                )
                
                # CEO Analysis
                ceo_prompt = f"""You are an experienced CEO with 25+ years of expertise. 
                Analyze this business challenge and provide strategic recommendations:
                
                Challenge: {user_input}
                
                Provide:
                1. Strategic Overview (2-3 sentences)
                2. Top 3 Strategic Recommendations
                3. Implementation Priority
                4. Expected Outcomes
                
                Be concise, professional, and actionable."""
                
                ceo_response = llm.invoke(ceo_prompt)
                
                st.write("💰 CFO Agent calculating financials...")
                
                cfo_prompt = f"""You are a seasoned CFO. Analyze the financial implications:
                
                Challenge: {user_input}
                
                Provide:
                1. Financial Impact Assessment
                2. Investment Required (estimate)
                3. ROI Projection
                4. Key Financial Risks
                
                Be specific with numbers where possible."""
                
                cfo_response = llm.invoke(cfo_prompt)
                
                st.write("🎯 Problem Solver crafting solutions...")
                
                solver_prompt = f"""You are a creative business problem solver. 
                Provide innovative solutions:
                
                Challenge: {user_input}
                
                Provide:
                1. Root Cause Analysis
                2. 3 Creative Solutions
                3. Quick Wins (next 30 days)
                4. Long-term Strategy
                
                Think outside the box."""
                
                solver_response = llm.invoke(solver_prompt)
                
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                # Display Results
                st.success("🎉 Strategic Analysis Generated Successfully!")
                
                # Tabs for each agent
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "👔 CEO Analysis", "💰 CFO Analysis", "🎯 Solutions"])
                
                with tab1:
                    st.markdown("### Executive Briefing")
                    st.markdown(f"**Challenge:** {user_input}")
                    st.markdown(f"**Analyzed by:** Multi-Agent Executive Team")
                    st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
                    st.divider()
                    st.markdown("### 🎯 Key Insights")
                    st.markdown(ceo_response.content[:500] + "...")
                
                with tab2:
                    st.markdown("### 👔 CEO Strategic Analysis")
                    st.markdown(ceo_response.content)
                
                with tab3:
                    st.markdown("### 💰 CFO Financial Analysis")
                    st.markdown(cfo_response.content)
                
                with tab4:
                    st.markdown("### 🎯 Creative Solutions")
                    st.markdown(solver_response.content)
                
                # Download button
                full_report = f"""
# StrategyAI Pro - Executive Analysis Report

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Challenge:** {user_input}

---

## 👔 CEO Strategic Analysis
{ceo_response.content}

---

## 💰 CFO Financial Analysis
{cfo_response.content}

---

## 🎯 Creative Solutions
{solver_response.content}

---
*Generated by StrategyAI Pro - https://strategyai-pro.streamlit.app*
"""
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=full_report,
                    file_name=f"strategy_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"Error: {str(e)}")
                st.info("💡 Tip: Check your API key and internet connection.")

# ═══════════════════════════════════════════════
# 🔚 FOOTER
# ═══════════════════════════════════════════════
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 2rem;'>
    <p>🚀 <b>StrategyAI Pro</b> — AI-Powered Executive Decision Platform</p>
    <p style='font-size: 0.85rem;'>Built with Streamlit, LangChain & Groq | © 2025</p>
</div>
""", unsafe_allow_html=True)