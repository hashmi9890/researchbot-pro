import streamlit as st
import os
from datetime import datetime

# ═══════════════════════════════════════════════
# 🔐 API KEY SETUP
# ═══════════════════════════════════════════════
try:
    # Try Streamlit Cloud Secrets first
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    # Fallback to environment
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ═══════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════
st.set_page_config(page_title="StrategyAI Pro", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .stApp {background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f0c29); color: #F9FAFB;}
    .stButton>button {background: linear-gradient(90deg, #6366F1, #8B5CF6); color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600;}
    .result-card {background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;}
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# 🎯 HEADER
# ═══════════════════════════════════════════════
st.title("🎯 StrategyAI Pro")
st.caption("Executive Decisions, Powered by AI")

# ═══════════════════════════════════════════════
# 🎛️ SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Control Center")
    
    if not GROQ_API_KEY:
        st.error("❌ API Key Missing!")
        st.info("Add GROQ_API_KEY in Streamlit Secrets")
        st.stop()  # Stop app if no key
    
    st.success("✅ API Connected")
    st.caption(f"Key: ...{GROQ_API_KEY[-4:]}")
    
    temp = st.slider("🎨 Creativity", 0.0, 1.0, 0.3, 0.1)
    st.divider()
    st.caption("© 2025 Abdullah Hashmi")

# ═══════════════════════════════════════════════
# 🤖 AGENTS
# ═══════════════════════════════════════════════
cols = st.columns(3)
for col, (icon, title, desc) in zip(cols, [
    ("👔", "CEO Agent", "Strategic Planning"),
    ("💰", "CFO Agent", "Financial Analysis"),
    ("🎯", "Solver", "Problem Solving")
]):
    with col:
        st.markdown(f"### {icon} {title}\n{desc}")

st.divider()

# ═══════════════════════════════════════════════
# 📝 INPUT
# ═══════════════════════════════════════════════
st.subheader("📝 Business Challenge")

query = st.text_area("Describe your challenge:", 
    placeholder="How to increase revenue by 50% without hiring...",
    height=100)

if st.button("🚀 Generate Strategy", use_container_width=True):
    if not query.strip():
        st.warning("⚠️ Please enter a challenge!")
    else:
        # ═══════════════════════════════════════════════
        # 🧠 AI PROCESSING (Direct Groq API)
        # ═══════════════════════════════════════════════
        with st.spinner("🚀 Deploying AI Agents... (30-60 sec)"):
            try:
                # Import here to catch errors
                import groq
                
                client = groq.Groq(api_key=GROQ_API_KEY)
                
                progress = st.empty()
                
                # CEO Analysis
                progress.text("👔 CEO Agent analyzing...")
                ceo_chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=temp,
                    messages=[{
                        "role": "system", 
                        "content": "You are an expert CEO with 25 years experience. Give strategic advice in 3-4 bullet points."
                    }, {
                        "role": "user",
                        "content": f"Analyze this business challenge and provide strategic recommendations:\n\n{query}"
                    }]
                )
                ceo_result = ceo_chat.choices[0].message.content
                
                # CFO Analysis
                progress.text("💰 CFO Agent calculating...")
                cfo_chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=temp,
                    messages=[{
                        "role": "system",
                        "content": "You are a CFO. Provide financial analysis and ROI estimates in 3-4 bullet points."
                    }, {
                        "role": "user",
                        "content": f"Analyze financial aspects:\n\n{query}"
                    }]
                )
                cfo_result = cfo_chat.choices[0].message.content
                
                # Problem Solver
                progress.text("🎯 Problem Solver thinking...")
                solver_chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=temp,
                    messages=[{
                        "role": "system",
                        "content": "You are a creative business consultant. Provide innovative solutions in 3-4 bullet points."
                    }, {
                        "role": "user",
                        "content": f"Suggest creative solutions for:\n\n{query}"
                    }]
                )
                solver_result = solver_chat.choices[0].message.content
                
                progress.empty()
                
                # ═══════════════════════════════════════════════
                # 📊 DISPLAY RESULTS
                # ═══════════════════════════════════════════════
                st.success("✅ Analysis Complete!")
                
                tab1, tab2, tab3 = st.tabs(["👔 CEO Strategy", "💰 CFO Analysis", "🎯 Solutions"])
                
                with tab1:
                    st.markdown(ceo_result)
                    
                with tab2:
                    st.markdown(cfo_result)
                    
                with tab3:
                    st.markdown(solver_result)
                
                # Download
                full_report = f"""# StrategyAI Pro Report
Generated: {datetime.now()}

## Challenge
{query}

## CEO Strategy
{ceo_result}

## CFO Analysis
{cfo_result}

## Creative Solutions
{solver_result}
"""
                st.download_button("📥 Download Report", full_report, 
                    f"strategy_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.error(f"Type: {type(e).__name__}")
                
                # Debug info
                with st.expander("🔍 Debug"):
                    import sys
                    st.write("Python:", sys.version)
                    try:
                        import groq
                        st.write("✅ Groq SDK installed")
                    except:
                        st.write("❌ Groq SDK NOT installed")