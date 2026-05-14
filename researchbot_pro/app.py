import streamlit as st
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time

# ═══════════════════════════════════════════════════════════
# 🔐 CONFIGURATION
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 🎨 CLAUDE-STYLE PREMIUM CSS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {font-family: 'Inter', sans-serif;}
    
    .stApp {
        background: #0f0f0f;
        color: #ececec;
    }
    
    /* Sidebar - Command Center */
    [data-testid="stSidebar"] {
        background: #1a1a1a;
        border-right: 1px solid #2d2d2d;
    }
    
    /* Cards */
    .agent-card {
        background: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 12px;
    }
    
    .agent-card:hover {
        border-color: #4f46e5;
        background: #1e1e2e;
        transform: translateX(5px);
    }
    
    .agent-card.active {
        border-color: #4f46e5;
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2b55 100%);
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.2);
    }
    
    /* Dashboard Cards */
    .metric-card {
        background: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4f46e5;
    }
    
    .metric-label {
        color: #888;
        font-size: 0.9rem;
        margin-top: 8px;
    }
    
    /* Chat Interface */
    .chat-container {
        background: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
    }
    
    .user-message {
        background: #2d2d2d;
        border-radius: 12px 12px 12px 4px;
        padding: 16px;
        margin: 12px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    
    .ai-message {
        background: #1e1e2e;
        border-left: 3px solid #4f46e5;
        border-radius: 12px 12px 4px 12px;
        padding: 16px;
        margin: 12px 0;
        max-width: 85%;
        float: left;
        clear: both;
    }
    
    /* Charts */
    .chart-container {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        border: 1px solid #2d2d2d;
    }
    
    /* Input Box */
    .stTextArea textarea {
        background: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-radius: 12px;
        color: white;
        font-size: 16px;
        padding: 16px;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    
    /* Hide defaults */
    #MainMenu, footer, .stDeployButton {visibility: hidden;}
    
    /* Clearfix */
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 🎛️ SESSION STATE (Auto-clear ke liye)
# ═══════════════════════════════════════════════════════════
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = "All Agents"
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""

# ═══════════════════════════════════════════════════════════
# 🎯 SIDEBAR - COMMAND CENTER (Interactive)
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎯 Command Center")
    st.markdown("---")
    
    # Agent Selection (Functional)
    st.markdown("### 🤖 Select Agent Mode")
    
    agents = [
        ("🎯 All Agents", "Comprehensive analysis using CEO, CFO & Solver"),
        ("👔 CEO Only", "Strategic vision & market positioning"),
        ("💰 CFO Only", "Financial deep-dive & ROI analysis"),
        ("🧩 Problem Solver", "Creative solutions & innovation")
    ]
    
    for i, (icon_name, desc) in enumerate(agents):
        is_active = st.session_state.selected_agent == icon_name
        
        if st.button(
            f"{icon_name}\n\n<small>{desc}</small>",
            key=f"agent_{i}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.selected_agent = icon_name
            st.session_state.messages = []  # Auto-clear previous
            st.session_state.analysis_done = False
            st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    creativity = st.slider("AI Creativity", 0.0, 1.0, 0.3, 0.1)
    
    if GROQ_API_KEY:
        st.success(f"🔌 Connected")
    else:
        st.error("❌ No API Key")
    
    st.markdown("---")
    st.caption("StrategyAI Pro v2.0")

# ═══════════════════════════════════════════════════════════
# 📊 MAIN DASHBOARD (Claude-style)
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-size: 2.5rem; font-weight: 700; margin: 0;'>
        <span style='color: #4f46e5;'>Strategy</span>AI Pro
    </h1>
    <p style='color: #888; margin-top: 8px;'>Executive Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Show selected agent badge
if st.session_state.selected_agent != "🎯 All Agents":
    st.info(f"**Mode:** {st.session_state.selected_agent} | Previous analyses auto-cleared")

# ═══════════════════════════════════════════════════════════
# 📈 METRICS DASHBOARD (Sample Data - Realistic)
# ═══════════════════════════════════════════════════════════
if not st.session_state.analysis_done:
    st.markdown("### 📊 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">24</div>
            <div class="metric-label">Strategies Generated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$2.4M</div>
            <div class="metric-label">Projected Savings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">94%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">3.2x</div>
            <div class="metric-label">Avg ROI</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Revenue Projection Chart
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Revenue Projection', 'Risk Assessment'),
        specs=[[{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # Line chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    current = [100, 105, 110, 108, 115, 120]
    projected = [100, 110, 125, 145, 170, 200]
    
    fig.add_trace(
        go.Scatter(x=months, y=current, name='Current', line=dict(color='#888')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=projected, name='With Strategy', line=dict(color='#4f46e5', width=4)),
        row=1, col=1
    )
    
    # Pie chart
    fig.add_trace(
        go.Pie(
            labels=['Market Risk', 'Financial', 'Operational', 'Growth'],
            values=[25, 35, 20, 20],
            hole=0.4,
            marker_colors=['#ef4444', '#f59e0b', '#3b82f6', '#10b981']
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ececec',
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 💬 CHAT INTERFACE
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### 💬 Business Challenge")

# Auto-clear logic: Agar naya input different hai to clear karo
new_query = st.text_area(
    "Describe your challenge:",
    placeholder="e.g., How can we increase revenue by 50% in 6 months without hiring...",
    height=100,
    key="input_box"
)

# Check if query changed
if new_query != st.session_state.current_query and new_query.strip():
    st.session_state.messages = []  # AUTO-CLEAR!
    st.session_state.analysis_done = False
    st.session_state.current_query = new_query

col_btn, col_clear = st.columns([4, 1])
with col_btn:
    analyze_btn = st.button("🚀 Generate Strategy", type="primary", use_container_width=True)
with col_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.analysis_done = False
        st.session_state.current_query = ""
        st.rerun()

# ═══════════════════════════════════════════════════════════
# 🧠 AI PROCESSING
# ═══════════════════════════════════════════════════════════
if analyze_btn and new_query.strip():
    if not GROQ_API_KEY:
        st.error("❌ Please add GROQ_API_KEY in Streamlit Secrets")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": new_query})
        
        with st.spinner(f"🤖 {st.session_state.selected_agent} analyzing..."):
            try:
                import groq
                client = groq.Groq(api_key=GROQ_API_KEY)
                
                # Prepare agent-specific prompts
                agent = st.session_state.selected_agent
                
                if "CEO" in agent:
                    system_msg = "You are a Fortune 500 CEO. Provide strategic analysis with bullet points."
                    temp = creativity
                elif "CFO" in agent:
                    system_msg = "You are a CFO. Provide financial analysis with numbers, ROI, and risk assessment."
                    temp = creativity
                elif "Solver" in agent:
                    system_msg = "You are a creative consultant. Provide innovative, out-of-box solutions."
                    temp = creativity + 0.2
                else:  # All agents
                    system_msg = """You are a team of CEO, CFO, and Problem Solver. Provide comprehensive analysis with:
                    1. Strategic Overview (CEO)
                    2. Financial Analysis (CFO)  
                    3. Creative Solutions (Problem Solver)
                    Use bullet points and be specific."""
                    temp = creativity
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=temp,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": new_query}
                    ]
                )
                
                ai_response = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.analysis_done = True
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════
# 📜 DISPLAY MESSAGES (Chat Style)
# ═══════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="clearfix">
            <div class="user-message">
                <strong>You</strong><br>{msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="clearfix">
            <div class="ai-message">
                <strong style='color: #4f46e5;'>🎯 StrategyAI</strong><br>
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Download button if analysis done
if st.session_state.analysis_done and st.session_state.messages:
    report = f"# Strategy Report\n\nQuery: {st.session_state.current_query}\n\nResponse:\n{st.session_state.messages[-1]['content']}"
    st.download_button(
        "📥 Download Report",
        report,
        f"strategy_{datetime.now().strftime('%H%M')}.md",
        use_container_width=True
    )

# ═══════════════════════════════════════════════════════════
# 📋 FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; font-size: 0.8rem;'>
    StrategyAI Pro | Built with Streamlit & Groq
</div>
""", unsafe_allow_html=True)