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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════
# 🎛️ SIDEBAR (Features & Settings)
# ═══════════════════════════════════════════════
with st.sidebar:
    st.title("🎯 Command Center")
    st.markdown("---")
    
    # Agent Selection
    st.subheader("🤖 Select Agent")
    agent_mode = st.radio(
        "Choose mode:",
        ["🎯 All Agents (Comprehensive)", "👔 CEO Only (Strategy)", "💰 CFO Only (Finance)", "🧩 Problem Solver (Creative)"],
        index=0
    )
    
    st.markdown("---")
    creativity = st.slider("AI Creativity Level", 0.0, 1.0, 0.3, 0.1)
    
    if GROQ_API_KEY:
        st.success("✅ API Key Connected")
    else:
        st.error("❌ API Key Missing in Secrets")
        
    st.markdown("---")
    st.caption("Built by Abdullah Hashmi")

# ═══════════════════════════════════════════════
# 🏠 MAIN INTERFACE
# ═══════════════════════════════════════════════
st.title("🎯 StrategyAI Pro")
st.caption("Executive Intelligence Platform - Ask anything about business strategy.")
st.markdown("---")

# 1. INPUT BOX (Top Pe)
# Hum session state use karenge taake clear kar saken
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

user_query = st.text_area(
    "💬 Describe your business challenge:",
    value=st.session_state.user_input,
    height=120,
    placeholder="e.g., How can we increase our SaaS revenue by 50% in 6 months without hiring more staff?",
    key="input_area" 
)

# 2. BUTTONS
col_btn, col_clear = st.columns([4, 1])

with col_btn:
    generate_btn = st.button("🚀 Generate Strategy", type="primary", use_container_width=True)

with col_clear:
    clear_btn = st.button("🗑️ Clear All", use_container_width=True)

# ═══════════════════════════════════════════════
# 🧠 LOGIC & PROCESSING
# ═══════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Button Logic
if clear_btn:
    st.session_state.messages = []
    st.session_state.user_input = ""
    st.rerun()

# Generate Button Logic
if generate_btn:
    if not user_query.strip():
        st.warning("⚠️ Please enter a challenge first!")
    elif not GROQ_API_KEY:
        st.error("❌ API Key missing! Add it in Streamlit Secrets.")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # AUTO-CLEAR INPUT BOX for next question
        st.session_state.user_input = "" 
        
        with st.spinner(f"🤖 {agent_mode.split(' ')[1]} is analyzing..."):
            try:
                import groq
                client = groq.Groq(api_key=GROQ_API_KEY)
                
                # Set System Prompt based on Agent
                if "CEO" in agent_mode:
                    sys_prompt = "You are a Fortune 500 CEO. Provide strategic analysis in bullet points."
                elif "CFO" in agent_mode:
                    sys_prompt = "You are a CFO. Provide financial analysis with numbers, ROI, and risk."
                elif "Solver" in agent_mode:
                    sys_prompt = "You are a creative consultant. Provide innovative, out-of-box solutions."
                else:
                    sys_prompt = "You are a team of CEO, CFO, and Problem Solver. Provide comprehensive analysis with sections for Strategy, Finance, and Solutions."

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=creativity,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": user_query}
                    ]
                )
                
                ai_response = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                # Refresh page to show result and clear input
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════
# 📜 DISPLAY CHAT HISTORY (Neeche Output)
# ═══════════════════════════════════════════════
if st.session_state.messages:
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.write(msg["content"])
            else:
                st.markdown(msg["content"])
                
    # Download Button at the end
    last_response = st.session_state.messages[-1]['content']
    st.download_button(
        label="📥 Download Report as Markdown",
        data=last_response,
        file_name=f"Strategy_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown"
    )