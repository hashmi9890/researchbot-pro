"""
╔══════════════════════════════════════════════════════════════╗
║        Executive Intelligence OS — ResearchBot Pro v3.0      ║
║   Research • Problem Solving • Analytics • CEO/CFO Reports   ║
║        File Upload • Image Analysis • Prompt Studio          ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import sys
import os
import json
import base64
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title = "Executive Intelligence OS",
    page_icon  = "🧠",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ── Project Path ─────────────────────────────────────────────
sys.path.append(str(Path(__file__).parent))

from src.config              import config
from src.graph.workflow      import ResearchWorkflow
from src.crew.problem_crew   import ProblemSolvingCrew
from src.crew.executive_crew import CEOReportCrew, CFOReportCrew, PromptEngineeringCrew
from src.analytics.data_loader import DataLoader
from src.analytics.charts      import ChartEngine
from src.prompts.templates     import PromptTemplates
# ── Absolute Paths ───────────────────────────────────
# ── Absolute Paths ───────────────────────────────────
BASE_DIR    = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0e0e1a; color: #e0e0e0; }
    .main-title {
        font-size: 2.8rem; font-weight: 900;
        background: linear-gradient(135deg, #00d2ff 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; letter-spacing: -1px;
    }
    .sub-title {
        text-align: center; color: #888;
        font-size: 1rem; margin-bottom: 2rem;
    }
    .card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2a2a4a; border-radius: 12px;
        padding: 1.5rem; margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff, #7b2ff7);
        color: white; border: none; font-weight: 600;
        border-radius: 8px; transition: all 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; transform: translateY(-1px); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#                        HEADER
# ══════════════════════════════════════════════════════════════

st.markdown('<p class="main-title">🧠 Executive Intelligence OS</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Research • Problem Solving • Analytics • CEO/CFO Reports • File & Image Analysis • Prompt Studio</p>',
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════════
#                        SIDEBAR
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🧠 Intelligence OS")
    st.markdown("---")

    # API Status
    try:
        config.validate()
        st.success("✅ API Connected")
    except ValueError:
        st.error("❌ GROQ_API_KEY Missing!")
        st.info("Add key to .env file")
        st.stop()

    st.info(f"🤖 **Model:** llama-3.3-70b\n\n🔧 **Engine:** Groq (Free)")
    st.markdown("---")

    # Mode Selector
    st.markdown("## 🎯 Select Mode")
    mode = st.selectbox(
        "Mode",
        [
            "🔬 Research Report",
            "🧩 Problem Solving",
            "📊 Data Analytics",
            "🖼️ Image Analysis",
            "📄 Document Analysis",
            "👔 CEO Report",
            "💰 CFO Report",
            "⚡ Prompt Engineering",
            "📁 File Manager",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Pipeline info
    mode_pipelines = {
        "🔬 Research Report"   : "Researcher → Analyst → Writer",
        "🧩 Problem Solving"    : "Clarifier → Solver → Risk Analyst",
        "📊 Data Analytics"    : "Upload CSV/Excel → Auto Analysis",
        "🖼️ Image Analysis"    : "Upload Image → AI Description + Insights",
        "📄 Document Analysis" : "Upload PDF/TXT/DOCX → AI Summary + Analysis",
        "👔 CEO Report"         : "Researcher → CEO Strategic Advisor",
        "💰 CFO Report"         : "CFO Financial Analyst",
        "⚡ Prompt Engineering" : "Prompt Engineer Agent",
        "📁 File Manager"      : "View + Download All Reports",
    }
    st.markdown(f"**Pipeline:**\n\n`{mode_pipelines.get(mode, '')}`")
    st.markdown("---")

    # Stats
    output_dir = OUTPUTS_DIR
    reports    = list(output_dir.glob("*.md")) if output_dir.exists() else []
    uploads    = list( UPLOADS_DIR.glob("*")) if UPLOADS_DIR.exists() else []

    col1, col2 = st.columns(2)
    col1.metric("📄 Reports", len(reports))
    col2.metric("📁 Uploads", len(uploads))


# ══════════════════════════════════════════════════════════════
#  HELPER: Save + Run Research
# ══════════════════════════════════════════════════════════════

def save_report(content: str, prefix: str = "report") -> str:
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = str(OUTPUTS_DIR / f"{prefix}_{ts}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def show_report(result: str, title: str = "Report", prefix: str = "report"):
    """Display report with tabs and download"""
    st.success("✅ Complete!")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Report", "📥 Export"])

    with tab1:
        st.markdown(f"### {title}")
        st.markdown(result)

    with tab2:
        path = save_report(result, prefix)
        st.success(f"💾 Saved: `{path}`")
        st.download_button(
            f"⬇️ Download {title}",
            data      = result,
            file_name = f"{prefix}_{datetime.now().strftime('%Y%m%d')}.md",
            mime      = "text/markdown",
            use_container_width = True,
        )


# ══════════════════════════════════════════════════════════════
#              MODE: RESEARCH REPORT
# ══════════════════════════════════════════════════════════════

if mode == "🔬 Research Report":
    st.markdown("## 🔬 Research Report Generator")

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. AI Agents in 2025, Pakistan Tech Ecosystem...",
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("🚀 Research", use_container_width=True)

    # Quick examples
    st.markdown("**💡 Quick Topics:**")
    ecols = st.columns(5)
    examples = [
        "AI Agents 2025", "EV Market", "Crypto Trends",
        "Climate Tech", "Pakistan Startups"
    ]
    for i, ex in enumerate(examples):
        with ecols[i]:
            if st.button(ex, key=f"res_{i}"):
                topic = ex
                run   = True

    if run and topic:
        with st.spinner("🤖 Research crew working... (2-5 mins)"):
            prog = st.progress(0)
            s1, s2, s3 = st.columns(3)
            s1.info("🔍 Validating...")
            prog.progress(15)

            try:
                wf     = ResearchWorkflow()
                result = wf.run(topic=topic)
                prog.progress(100)
                s1.success("✅ Validated")
                s2.success("✅ Researched")
                s3.success("✅ Written")

                if result.get("research_report"):
                    m1, m2, m3 = st.columns(3)
                    m1.metric("📝 Words",  f"{result.get('word_count', 0):,}")
                    m2.metric("🤖 Agents", "3")
                    m3.metric("💾 Status", "Saved ✅")
                    show_report(
                        result["research_report"],
                        title  = f"Research: {topic}",
                        prefix = "research"
                    )
                else:
                    st.error(f"❌ {result.get('error_message')}")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: PROBLEM SOLVING
# ══════════════════════════════════════════════════════════════

elif mode == "🧩 Problem Solving":
    st.markdown("## 🧩 Business Problem Solver")
    st.markdown("Describe your problem → Root cause + Solution roadmap")

    with st.form("problem_form"):
        col1, col2 = st.columns(2)
        with col1:
            problem  = st.text_area("🔴 Problem Statement *",
                       placeholder="e.g. Sales dropped 40% in last 3 months...",
                       height=120)
            goal     = st.text_input("🎯 Goal",
                       placeholder="e.g. Recover to $50K MRR in 90 days")
            industry = st.selectbox("🏢 Industry", [
                "Tech/SaaS", "E-commerce", "Finance",
                "Healthcare", "Marketing Agency",
                "Manufacturing", "Real Estate", "Other"
            ])
        with col2:
            constraints = st.text_area("⛔ Constraints",
                          placeholder="e.g. Budget $10K, team of 3...",
                          height=80)
            budget   = st.text_input("💰 Budget",
                       placeholder="e.g. $5,000/month")
            timeline = st.selectbox("⏰ Timeline", [
                "1 week", "2 weeks", "1 month",
                "3 months", "6 months", "1 year"
            ])
            urgency  = st.select_slider("🔥 Urgency",
                       options=["Low", "Medium", "High", "Critical"])

        # File attachment option
        st.markdown("### 📎 Attach Supporting File (Optional)")
        attached_file = st.file_uploader(
            "Upload relevant doc/data",
            type=["txt", "csv", "xlsx", "pdf", "md"],
            key="problem_file"
        )

        submit = st.form_submit_button("🧩 Solve Problem", use_container_width=True)

    if submit and problem:
        # Add file content to context if attached
        extra_context = ""
        if attached_file:
            if attached_file.name.endswith(".txt") or attached_file.name.endswith(".md"):
                extra_context = f"\n\nAttached File Content:\n{attached_file.read().decode('utf-8')[:2000]}"
            elif attached_file.name.endswith(".csv"):
                df = pd.read_csv(attached_file)
                extra_context = f"\n\nAttached Data Preview:\n{df.head(10).to_string()}"

        problem_data = {
            "problem"    : problem + extra_context,
            "goal"       : goal,
            "industry"   : industry,
            "constraints": constraints,
            "budget"     : budget,
            "timeline"   : timeline,
            "urgency"    : urgency,
        }

        with st.spinner("🤖 Problem solving crew analyzing... (2-5 mins)"):
            try:
                crew   = ProblemSolvingCrew(problem_data=problem_data)
                result = crew.run()
                show_report(result, title="Problem Solving Report", prefix="problem")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: DATA ANALYTICS
# ══════════════════════════════════════════════════════════════

elif mode == "📊 Data Analytics":
    st.markdown("## 📊 Data Analytics Dashboard")
    st.markdown("Upload CSV or Excel → Auto analysis, KPIs, Charts, AI Insights.")

    uploaded = st.file_uploader(
        "📁 Upload Dataset",
        type   = ["csv", "xlsx", "xls"],
        help   = "Supported: CSV, Excel (.xlsx, .xls) | Max 50MB"
    )

    if uploaded:
        save_path = UPLOADS_DIR / uploaded.name
        save_path.write_bytes(uploaded.getvalue())

        try:
            loader  = DataLoader(str(save_path))
            df      = loader.load()
            profile = loader.profile()
            kpis    = loader.get_kpis()
            charts  = ChartEngine(df)

            # Overview
            st.markdown("### 📊 Dataset Overview")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("📋 Rows",        f"{profile['rows']:,}")
            c2.metric("📐 Columns",     profile['columns'])
            c3.metric("🔢 Numeric",     len(profile['numeric_cols']))
            c4.metric("🔤 Categorical", len(profile['categorical_cols']))
            c5.metric("⚠️ Missing",     sum(profile['missing_values'].values()))

            st.markdown("---")

            tabs = st.tabs([
                "👀 Preview",
                "📊 KPIs",
                "📈 Charts",
                "🔍 Quality",
                "🤖 AI Insights",
                "📥 Export",
            ])

            # Tab 1: Preview
            with tabs[0]:
                rows_to_show = st.slider("Rows to show", 5, min(100, profile['rows']), 20)
                st.dataframe(df.head(rows_to_show), use_container_width=True)

                # Column info
                st.markdown("### 📋 Column Info")
                col_info = pd.DataFrame({
                    "Column" : df.columns,
                    "Type"   : df.dtypes.astype(str).values,
                    "Missing": df.isnull().sum().values,
                    "Unique" : df.nunique().values,
                })
                st.dataframe(col_info, use_container_width=True)

            # Tab 2: KPIs
            with tabs[1]:
                if kpis:
                    kpi_df = pd.DataFrame(kpis).T
                    st.dataframe(kpi_df, use_container_width=True)
                    fig = charts.kpi_summary_chart(profile['numeric_cols'])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No numeric columns found.")

            # Tab 3: Charts
            with tabs[2]:
                # Correlation
                fig_corr = charts.correlation_heatmap()
                if fig_corr:
                    st.plotly_chart(fig_corr, use_container_width=True)

                # Distribution
                if profile['numeric_cols']:
                    st.markdown("### 📊 Distribution")
                    selected = st.selectbox("Select column", profile['numeric_cols'])
                    fig_dist = charts.distribution_chart(selected)
                    if fig_dist:
                        st.plotly_chart(fig_dist, use_container_width=True)

                # Trend
                if len(df.columns) >= 2:
                    st.markdown("### 📉 Trend")
                    tc1, tc2 = st.columns(2)
                    with tc1:
                        x_col = st.selectbox("X Axis", df.columns.tolist())
                    with tc2:
                        y_col = st.selectbox("Y Axis", profile['numeric_cols'] or df.columns.tolist())
                    fig_trend = charts.trend_chart(x_col, y_col)
                    if fig_trend:
                        st.plotly_chart(fig_trend, use_container_width=True)

                # Missing values chart
                fig_miss = charts.missing_values_chart()
                if fig_miss:
                    st.markdown("### ⚠️ Missing Values")
                    st.plotly_chart(fig_miss, use_container_width=True)

            # Tab 4: Quality
            with tabs[3]:
                st.markdown("### 🔍 Data Quality Report")
                missing_data = {k: v for k, v in profile['missing_values'].items() if v > 0}
                if missing_data:
                    st.warning(f"⚠️ {len(missing_data)} columns have missing values")
                    miss_df = pd.DataFrame({
                        "Column" : list(missing_data.keys()),
                        "Missing": list(missing_data.values()),
                        "Pct %"  : [profile['missing_pct'][k] for k in missing_data],
                    })
                    st.dataframe(miss_df, use_container_width=True)
                else:
                    st.success("✅ No missing values!")

                if profile['duplicates'] > 0:
                    st.warning(f"⚠️ {profile['duplicates']} duplicate rows")
                else:
                    st.success("✅ No duplicates!")

            # Tab 5: AI Insights
            with tabs[4]:
                st.markdown("### 🤖 AI-Generated Insights")
                if st.button("🤖 Generate AI Insights", use_container_width=True):
                    summary = (
                        f"Dataset: {profile['rows']} rows, {profile['columns']} cols\n"
                        f"Numeric: {profile['numeric_cols']}\n"
                        f"Categorical: {profile['categorical_cols']}\n"
                        f"Missing: {sum(profile['missing_values'].values())}\n"
                        f"KPIs: {json.dumps(kpis, indent=2)[:1500]}"
                    )
                    with st.spinner("🤖 AI analyzing..."):
                        try:
                            crew   = CEOReportCrew(context=summary, company="Data Analysis")
                            result = crew.run()
                            st.markdown(result)
                            show_report(result, "Data Insights", "data_insights")
                        except Exception as e:
                            st.error(f"❌ {e}")

            # Tab 6: Export
            with tabs[5]:
                st.markdown("### 📥 Export Data")
                # CSV Export
                csv_data = df.to_csv(index=False)
                st.download_button(
                    "⬇️ Download CSV",
                    data      = csv_data,
                    file_name = f"data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime      = "text/csv",
                    use_container_width = True,
                )
                # Profile JSON
                profile_json = json.dumps(
                    {k: v for k, v in profile.items() if k != "summary_stats"},
                    indent=2
                )
                st.download_button(
                    "⬇️ Download Profile JSON",
                    data      = profile_json,
                    file_name = "data_profile.json",
                    mime      = "application/json",
                    use_container_width = True,
                )

        except Exception as e:
            st.error(f"❌ File error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: IMAGE ANALYSIS
# ══════════════════════════════════════════════════════════════

elif mode == "🖼️ Image Analysis":
    st.markdown("## 🖼️ Image Analysis")
    st.markdown("Upload image → Describe + analyze → Get AI insights")

    col1, col2 = st.columns([1, 1])

    with col1:
        image_file = st.file_uploader(
            "📸 Upload Image",
            type   = ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
            help   = "Supported: JPG, PNG, GIF, BMP, WEBP"
        )

        if image_file:
            st.image(image_file, caption=image_file.name, use_container_width=True)
            st.info(f"📁 File: `{image_file.name}`\n\n📊 Size: `{image_file.size/1024:.1f} KB`")

    with col2:
        st.markdown("### 🎯 Analysis Options")
        analysis_type = st.selectbox("Analysis Type", [
            "General Description",
            "Business / Marketing Analysis",
            "Data Visualization Analysis",
            "Product Analysis",
            "Brand & Logo Analysis",
            "Custom Analysis",
        ])

        custom_prompt = ""
        if analysis_type == "Custom Analysis":
            custom_prompt = st.text_area(
                "Custom Instructions",
                placeholder="Describe what you want to analyze...",
                height=100,
            )

        image_context = st.text_area(
            "📝 Additional Context (Optional)",
            placeholder="e.g. This is our product packaging...",
            height=80,
        )

        analyze_btn = st.button("🖼️ Analyze Image", use_container_width=True)

    if analyze_btn and image_file:
        # Since Groq/LLaMA text model — we describe via text context
        analysis_prompt = custom_prompt if custom_prompt else analysis_type

        full_context = (
            f"Image File: {image_file.name}\n"
            f"Analysis Type: {analysis_prompt}\n"
            f"Additional Context: {image_context}\n\n"
            f"Note: Provide detailed {analysis_type} based on the image name and context provided. "
            f"Give professional insights and recommendations."
        )

        with st.spinner("🤖 Analyzing..."):
            try:
                crew   = CEOReportCrew(
                    context = full_context,
                    company = "Image Analysis"
                )
                result = crew.run()
                show_report(result, "Image Analysis Report", "image_analysis")

                # Save image to uploads
                save_path = UPLOADS_DIR / image_file.name
                save_path.write_bytes(image_file.getvalue())
                st.success(f"✅ Image saved: `{save_path}`")

            except Exception as e:
                st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: DOCUMENT ANALYSIS
# ══════════════════════════════════════════════════════════════

elif mode == "📄 Document Analysis":
    st.markdown("## 📄 Document Analysis")
    st.markdown("Upload document → AI summary + key insights + action items")

    doc_file = st.file_uploader(
        "📄 Upload Document",
        type = ["txt", "md", "csv", "pdf"],
        help = "Supported: TXT, Markdown, CSV | Max 10MB"
    )

    if doc_file:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"📁 **File:** {doc_file.name} | 📊 **Size:** {doc_file.size/1024:.1f} KB")

        with col2:
            doc_analysis_type = st.selectbox("Analysis Mode", [
                "Executive Summary",
                "Key Insights",
                "Action Items",
                "SWOT Analysis",
                "Financial Analysis",
                "Risk Assessment",
                "Full Report",
            ])

        # Read content
        content = ""
        try:
            if doc_file.name.endswith((".txt", ".md")):
                content = doc_file.read().decode("utf-8")
            elif doc_file.name.endswith(".csv"):
                df      = pd.read_csv(doc_file)
                content = f"CSV Data Preview:\n{df.head(20).to_string()}\n\nStats:\n{df.describe().to_string()}"
            else:
                content = f"Document: {doc_file.name} (Binary file — analyze by filename and type)"
        except Exception:
            content = f"Document: {doc_file.name}"

        # Preview
        if content and len(content) < 5000:
            with st.expander("📖 Document Preview"):
                st.text(content[:2000])

        analyze_doc = st.button("📄 Analyze Document", use_container_width=True)

        if analyze_doc:
            context = (
                f"Document: {doc_file.name}\n"
                f"Analysis Type: {doc_analysis_type}\n\n"
                f"Content:\n{content[:3000]}"
            )

            with st.spinner(f"🤖 Running {doc_analysis_type}..."):
                try:
                    crew   = CEOReportCrew(
                        context = context,
                        company = doc_file.name
                    )
                    result = crew.run()
                    show_report(result, f"Document: {doc_analysis_type}", "doc_analysis")

                    # Save to uploads
                    save_path = UPLOADS_DIR / doc_file.name
                    save_path.write_bytes(doc_file.getvalue())

                except Exception as e:
                    st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: CEO REPORT
# ══════════════════════════════════════════════════════════════

elif mode == "👔 CEO Report":
    st.markdown("## 👔 CEO Strategic Report Generator")

    with st.form("ceo_form"):
        col1, col2 = st.columns(2)
        with col1:
            company  = st.text_input("🏢 Company Name",
                       placeholder="e.g. TechCo, My Agency...")
            context  = st.text_area("📋 Business Context *",
                       placeholder=(
                           "Current situation:\n"
                           "- What is your business?\n"
                           "- Revenue / users / metrics\n"
                           "- Key challenges\n"
                           "- Decision needed"
                       ), height=180)
            industry = st.selectbox("Industry", [
                "Tech/SaaS", "E-commerce", "Finance",
                "Healthcare", "Marketing", "Other"
            ])
        with col2:
            stage    = st.selectbox("Stage", [
                "Idea", "MVP", "Seed",
                "Series A", "Growth", "Scale"
            ])
            revenue  = st.text_input("Monthly Revenue", placeholder="$50,000")
            team     = st.text_input("Team Size", placeholder="12 people")
            market   = st.text_input("Target Market", placeholder="SMBs in USA")

            # File attachment
            st.markdown("### 📎 Attach Data (Optional)")
            ceo_file = st.file_uploader(
                "Supporting file",
                type=["txt", "csv", "md"],
                key="ceo_file"
            )

        generate = st.form_submit_button("👔 Generate CEO Report", use_container_width=True)

    if generate and context:
        extra = ""
        if ceo_file:
            try:
                extra = f"\n\nAttached Data:\n{ceo_file.read().decode('utf-8')[:1500]}"
            except Exception:
                pass

        full_context = (
            f"Company: {company} | Industry: {industry}\n"
            f"Stage: {stage} | Revenue: {revenue}\n"
            f"Team: {team} | Market: {market}\n\n"
            f"Context:\n{context}{extra}"
        )

        with st.spinner("👔 CEO advisor preparing report..."):
            try:
                crew   = CEOReportCrew(context=full_context, company=company)
                result = crew.run()
                show_report(result, f"CEO Report: {company}", "ceo_report")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: CFO REPORT
# ══════════════════════════════════════════════════════════════

elif mode == "💰 CFO Report":
    st.markdown("## 💰 CFO Financial Report Generator")

    with st.form("cfo_form"):
        col1, col2 = st.columns(2)
        with col1:
            company     = st.text_input("🏢 Company", placeholder="TechCo...")
            revenue     = st.text_input("💵 Monthly Revenue", placeholder="$120,000")
            cogs        = st.text_input("🏭 COGS", placeholder="$45,000")
            opex        = st.text_input("💸 Monthly OpEx", placeholder="$60,000")
            cash        = st.text_input("🏦 Cash in Bank", placeholder="$500,000")
        with col2:
            growth_rate = st.text_input("📈 MoM Growth", placeholder="15%")
            churn       = st.text_input("📉 Monthly Churn", placeholder="5%")
            ltv         = st.text_input("💎 Customer LTV", placeholder="$2,400")
            cac         = st.text_input("🎯 Customer CAC", placeholder="$300")

            # CSV Upload for financials
            st.markdown("### 📊 Upload Financial Data (Optional)")
            cfo_file = st.file_uploader(
                "CSV/Excel with financial data",
                type=["csv", "xlsx"],
                key="cfo_file"
            )

        extra = st.text_area("📋 Additional Context", height=80,
                 placeholder="Any other financial details...")

        generate = st.form_submit_button("💰 Generate CFO Report", use_container_width=True)

    if generate:
        csv_data = ""
        if cfo_file:
            try:
                df       = pd.read_csv(cfo_file) if cfo_file.name.endswith(".csv") else pd.read_excel(cfo_file)
                csv_data = f"\n\nFinancial Data:\n{df.to_string()[:2000]}"
            except Exception:
                pass

        financial_context = (
            f"Company: {company}\n"
            f"Revenue: {revenue} | COGS: {cogs} | OpEx: {opex}\n"
            f"Cash: {cash} | Growth: {growth_rate} | Churn: {churn}\n"
            f"LTV: {ltv} | CAC: {cac}\n\n"
            f"{extra}{csv_data}"
        )

        with st.spinner("💰 CFO analyst working..."):
            try:
                crew   = CFOReportCrew(financial_context=financial_context, company=company)
                result = crew.run()
                show_report(result, f"CFO Report: {company}", "cfo_report")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: PROMPT ENGINEERING
# ══════════════════════════════════════════════════════════════

elif mode == "⚡ Prompt Engineering":
    st.markdown("## ⚡ Prompt Engineering Studio")

    col1, col2 = st.columns([2, 1])
    with col1:
        original_prompt = st.text_area(
            "📝 Your Original Prompt",
            placeholder="Paste your prompt here...",
            height=200,
        )

        # File upload for prompt
        prompt_file = st.file_uploader(
            "📄 Or upload prompt from file (.txt)",
            type=["txt", "md"],
        )
        if prompt_file:
            original_prompt = prompt_file.read().decode("utf-8")
            st.success(f"✅ Loaded from: {prompt_file.name}")

    with col2:
        use_case = st.selectbox("🎯 Use Case", [
            "Content Writing",
            "Data Analysis",
            "Code Generation",
            "Sales & Marketing",
            "Research",
            "Customer Support",
            "CEO/CFO Reports",
            "Problem Solving",
            "General",
        ])

        st.markdown("### 📚 Quick Templates")
        templates = PromptTemplates.analysis_templates()
        selected  = st.selectbox("Templates", ["None"] + list(templates.keys()))
        if selected != "None":
            original_prompt = templates[selected]
            st.info(f"✅ Template loaded: {selected}")

    optimize = st.button("⚡ Optimize Prompt", use_container_width=True)

    if optimize and original_prompt:
        with st.spinner("⚡ Prompt engineer optimizing..."):
            try:
                crew   = PromptEngineeringCrew(
                    original_prompt = original_prompt,
                    use_case        = use_case
                )
                result = crew.run()

                tab1, tab2, tab3 = st.tabs([
                    "⚡ Optimized",
                    "🔄 Comparison",
                    "📥 Export"
                ])
                with tab1:
                    st.success("✅ Prompt Optimized!")
                    st.markdown(result)

                with tab2:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("### ❌ Original")
                        st.code(original_prompt, language="text")
                    with c2:
                        st.markdown("### ✅ Optimized")
                        st.code(result[:1000], language="text")

                with tab3:
                    path = save_report(result, "prompt_optimization")
                    st.success(f"💾 Saved: `{path}`")
                    st.download_button(
                        "⬇️ Download Optimized Prompt",
                        data      = result,
                        file_name = f"prompt_{use_case}.md",
                        mime      = "text/markdown",
                        use_container_width = True,
                    )
            except Exception as e:
                st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════════════════════
#              MODE: FILE MANAGER
# ══════════════════════════════════════════════════════════════

elif mode == "📁 File Manager":
    st.markdown("## 📁 File Manager")
    st.markdown("View, download, and manage all reports and uploads.")

    tab1, tab2 = st.tabs(["📄 Reports", "📁 Uploads"])

    with tab1:
        st.markdown("### 📄 Generated Reports")
        reports = sorted(OUTPUTS_DIR.glob("*.md"), reverse=True)

        if not reports:
            st.info("No reports yet. Generate one from any mode!")
        else:
            st.success(f"✅ {len(reports)} reports found")
            for report in reports:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    size = report.stat().st_size / 1024
                    st.markdown(f"📄 `{report.name}` — {size:.1f} KB")
                with col2:
                    content = report.read_text(encoding="utf-8")
                    st.download_button(
                        "⬇️ Download",
                        data      = content,
                        file_name = report.name,
                        mime      = "text/markdown",
                        key       = f"dl_{report.name}",
                    )
                with col3:
                    if st.button("👀 Preview", key=f"prev_{report.name}"):
                        st.markdown(content[:2000])

    with tab2:
        st.markdown("### 📁 Uploaded Files")
        uploads = list(UPLOADS_DIR.glob("*"))

        if not uploads:
            st.info("No uploads yet.")
        else:
            st.success(f"✅ {len(uploads)} files")
            for f in uploads:
                size = f.stat().st_size / 1024
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"📁 `{f.name}` — {size:.1f} KB")
                with col2:
                    st.download_button(
                        "⬇️",
                        data      = f.read_bytes(),
                        file_name = f.name,
                        key       = f"upl_{f.name}",
                    )


# ══════════════════════════════════════════════════════════════
#                      FOOTER
# ══════════════════════════════════════════════════════════════

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.markdown("**🧠 Executive Intelligence OS v3.0**")
c2.markdown("LangGraph + CrewAI + Groq LLM")
c3.markdown(f"*{datetime.now().strftime('%B %d, %Y — %I:%M %p')}*")