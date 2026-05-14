"""
╔══════════════════════════════════════════════════════════════╗
║         Executive Deep Dashboard — Full Analytics OS         ║
║     KPIs • Charts • HR • Finance • AI Insights • Reports     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime, timedelta
import json
import sys

# ── Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title = "Executive Deep Dashboard",
    page_icon  = "📊",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

sys.path.append(str(Path(__file__).parent))
BASE_DIR    = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

from src.config import config
from src.crew.executive_crew import CEOReportCrew, CFOReportCrew

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: #050510; }

    .dash-title {
        font-size: 2.2rem; font-weight: 900;
        background: linear-gradient(135deg, #00d2ff, #7b2ff7, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .kpi-card {
        background: linear-gradient(135deg, #0d0d1a, #1a1a3e);
        border: 1px solid #2a2a5a;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 900;
        color: #00d2ff;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-delta-up   { color: #4ade80; font-size: 0.8rem; }
    .kpi-delta-down { color: #f87171; font-size: 0.8rem; }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #00d2ff;
        border-left: 4px solid #7b2ff7;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    .insight-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #0d0d1a, #1a1a3e);
        border: 1px solid #2a2a5a;
        border-radius: 12px;
        padding: 1rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#                    SAMPLE DATA GENERATORS
# ══════════════════════════════════════════════════════════════

@st.cache_data
def generate_financial_data(months: int = 12) -> pd.DataFrame:
    np.random.seed(42)
    dates   = pd.date_range(end=datetime.now(), periods=months, freq="MS")
    revenue = np.cumsum(np.random.randint(5000, 15000, months)) + 50000
    costs   = revenue * np.random.uniform(0.45, 0.65, months)
    profit  = revenue - costs
    return pd.DataFrame({
        "Month"      : dates.strftime("%b %Y"),
        "Revenue"    : revenue.astype(int),
        "Costs"      : costs.astype(int),
        "Profit"     : profit.astype(int),
        "Margin %"   : (profit / revenue * 100).round(1),
        "Customers"  : np.random.randint(100, 500, months),
        "Churn %"    : np.random.uniform(2, 8, months).round(1),
        "CAC"        : np.random.randint(200, 600, months),
        "LTV"        : np.random.randint(1500, 4000, months),
    })


@st.cache_data
def generate_hr_data(employees: int = 150) -> pd.DataFrame:
    np.random.seed(42)
    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
    levels      = ["Junior", "Mid", "Senior", "Lead", "Manager", "Director"]
    return pd.DataFrame({
        "Employee ID"  : range(1001, 1001 + employees),
        "Department"   : np.random.choice(departments, employees),
        "Level"        : np.random.choice(levels, employees),
        "Salary"       : np.random.randint(40000, 180000, employees),
        "Performance"  : np.random.uniform(2.5, 5.0, employees).round(1),
        "Tenure (yrs)" : np.random.uniform(0.5, 15, employees).round(1),
        "Satisfaction" : np.random.uniform(3.0, 5.0, employees).round(1),
        "Training hrs" : np.random.randint(10, 120, employees),
        "Attrition Risk": np.random.choice(["Low", "Medium", "High"], employees, p=[0.6, 0.3, 0.1]),
        "Gender"       : np.random.choice(["Male", "Female", "Other"], employees, p=[0.52, 0.45, 0.03]),
        "Age"          : np.random.randint(22, 60, employees),
        "Remote"       : np.random.choice(["Yes", "No", "Hybrid"], employees),
    })


@st.cache_data
def generate_sales_data(records: int = 200) -> pd.DataFrame:
    np.random.seed(42)
    products  = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    regions   = ["North", "South", "East", "West", "Central"]
    channels  = ["Online", "Direct", "Partner", "Reseller"]
    dates     = pd.date_range(end=datetime.now(), periods=records, freq="D")
    return pd.DataFrame({
        "Date"     : dates,
        "Product"  : np.random.choice(products, records),
        "Region"   : np.random.choice(regions, records),
        "Channel"  : np.random.choice(channels, records),
        "Revenue"  : np.random.randint(1000, 50000, records),
        "Units"    : np.random.randint(1, 100, records),
        "Discount %" : np.random.uniform(0, 30, records).round(1),
        "Profit"   : np.random.randint(200, 15000, records),
        "Leads"    : np.random.randint(5, 200, records),
        "Converted": np.random.randint(1, 50, records),
    })


# ══════════════════════════════════════════════════════════════
#                        HEADER
# ══════════════════════════════════════════════════════════════

st.markdown('<p class="dash-title">📊 Executive Deep Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    f"<center style='color:#555;'>Last updated: {datetime.now().strftime('%B %d, %Y — %I:%M %p')}</center>",
    unsafe_allow_html=True
)
st.markdown("")


# ══════════════════════════════════════════════════════════════
#                        SIDEBAR
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 📊 Deep Dashboard")
    st.markdown("---")

    # API Status
    try:
        config.validate()
        st.success("✅ AI Connected")
    except ValueError:
        st.warning("⚠️ AI Offline")

    st.markdown("---")

    # Dashboard selector
    st.markdown("## 🎯 Dashboard")
    dashboard = st.selectbox("Select", [
        "🏠 Executive Overview",
        "💰 Financial Intelligence",
        "👥 HR Analytics",
        "📈 Sales Intelligence",
        "📊 Custom Data Upload",
        "🤖 AI Report Generator",
    ], label_visibility="collapsed")

    st.markdown("---")

    # Date range filter
    st.markdown("## 📅 Date Range")
    date_range = st.selectbox("Period", [
        "Last 30 Days",
        "Last 3 Months",
        "Last 6 Months",
        "Last 12 Months",
        "Year to Date",
    ])

    st.markdown("---")

    # Quick metrics
    fin_df = generate_financial_data()
    st.metric("💵 Total Revenue", f"${fin_df['Revenue'].sum():,.0f}")
    st.metric("📈 Avg Margin",    f"{fin_df['Margin %'].mean():.1f}%")
    st.metric("👥 Employees",     "150")


# ══════════════════════════════════════════════════════════════
#           DASHBOARD 1: EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════

if dashboard == "🏠 Executive Overview":

    fin_df  = generate_financial_data()
    hr_df   = generate_hr_data()
    sales_df= generate_sales_data()

    # ── Top KPIs ─────────────────────────────────────
    st.markdown('<p class="section-header">📌 Executive KPIs</p>', unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("💵 Revenue",      f"${fin_df['Revenue'].iloc[-1]:,.0f}",
              f"+{fin_df['Revenue'].pct_change().iloc[-1]*100:.1f}%")
    k2.metric("💰 Profit",       f"${fin_df['Profit'].iloc[-1]:,.0f}",
              f"+{fin_df['Profit'].pct_change().iloc[-1]*100:.1f}%")
    k3.metric("📊 Margin",       f"{fin_df['Margin %'].iloc[-1]:.1f}%")
    k4.metric("👥 Employees",    f"{len(hr_df)}")
    k5.metric("🎯 Satisfaction", f"{hr_df['Satisfaction'].mean():.1f}/5")
    k6.metric("⚠️ Attrition",   f"{(hr_df['Attrition Risk']=='High').sum()} at risk")

    st.markdown("---")

    # ── Revenue + Profit Trend ────────────────────────
    st.markdown('<p class="section-header">📈 Revenue & Profit Trend</p>', unsafe_allow_html=True)

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(
        x=fin_df["Month"], y=fin_df["Revenue"],
        name="Revenue", marker_color="#00d2ff", opacity=0.8
    ))
    fig_rev.add_trace(go.Bar(
        x=fin_df["Month"], y=fin_df["Costs"],
        name="Costs", marker_color="#ff6b6b", opacity=0.8
    ))
    fig_rev.add_trace(go.Scatter(
        x=fin_df["Month"], y=fin_df["Profit"],
        name="Profit", line=dict(color="#4ade80", width=3),
        mode="lines+markers"
    ))
    fig_rev.update_layout(
        template="plotly_dark", barmode="group",
        plot_bgcolor="#050510", paper_bgcolor="#050510",
        legend=dict(orientation="h", y=1.1),
        height=400,
    )
    st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("---")

    # ── 4 Mini Charts ────────────────────────────────
    st.markdown('<p class="section-header">🔍 Deep Insights</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Margin trend
        fig_margin = px.area(
            fin_df, x="Month", y="Margin %",
            title="Profit Margin Trend (%)",
            color_discrete_sequence=["#7b2ff7"],
            template="plotly_dark",
        )
        fig_margin.update_layout(
            plot_bgcolor="#050510", paper_bgcolor="#0d0d1a", height=300
        )
        st.plotly_chart(fig_margin, use_container_width=True)

        # Department distribution
        dept_counts = hr_df["Department"].value_counts()
        fig_dept = px.pie(
            values=dept_counts.values,
            names=dept_counts.index,
            title="Headcount by Department",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            template="plotly_dark",
        )
        fig_dept.update_layout(
            plot_bgcolor="#050510", paper_bgcolor="#0d0d1a", height=300
        )
        st.plotly_chart(fig_dept, use_container_width=True)

    with col2:
        # Sales by region
        region_sales = sales_df.groupby("Region")["Revenue"].sum().reset_index()
        fig_region = px.bar(
            region_sales, x="Region", y="Revenue",
            title="Revenue by Region",
            color="Revenue",
            color_continuous_scale="Viridis",
            template="plotly_dark",
        )
        fig_region.update_layout(
            plot_bgcolor="#050510", paper_bgcolor="#0d0d1a", height=300
        )
        st.plotly_chart(fig_region, use_container_width=True)

        # LTV vs CAC
        fig_ltv = go.Figure()
        fig_ltv.add_trace(go.Scatter(
            x=fin_df["Month"], y=fin_df["LTV"],
            name="LTV", line=dict(color="#4ade80", width=2),
            fill="tonexty",
        ))
        fig_ltv.add_trace(go.Scatter(
            x=fin_df["Month"], y=fin_df["CAC"],
            name="CAC", line=dict(color="#ff6b6b", width=2),
        ))
        fig_ltv.update_layout(
            title="LTV vs CAC Ratio",
            template="plotly_dark",
            plot_bgcolor="#050510", paper_bgcolor="#0d0d1a", height=300,
        )
        st.plotly_chart(fig_ltv, use_container_width=True)

    st.markdown("---")

    # ── AI Executive Summary ──────────────────────────
    st.markdown('<p class="section-header">🤖 AI Executive Summary</p>', unsafe_allow_html=True)

    if st.button("🤖 Generate AI Executive Summary", use_container_width=True):
        summary = (
            f"Business Performance Summary:\n"
            f"Total Revenue: ${fin_df['Revenue'].sum():,.0f}\n"
            f"Total Profit: ${fin_df['Profit'].sum():,.0f}\n"
            f"Avg Margin: {fin_df['Margin %'].mean():.1f}%\n"
            f"Total Employees: {len(hr_df)}\n"
            f"Avg Satisfaction: {hr_df['Satisfaction'].mean():.1f}/5\n"
            f"High Attrition Risk: {(hr_df['Attrition Risk']=='High').sum()}\n"
            f"Total Sales Revenue: ${sales_df['Revenue'].sum():,.0f}\n"
        )
        with st.spinner("🤖 AI generating executive summary..."):
            try:
                crew   = CEOReportCrew(context=summary, company="Executive Dashboard")
                result = crew.run()
                st.markdown(result)
                path = OUTPUTS_DIR / f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                path.write_text(result, encoding="utf-8")
                st.download_button("⬇️ Download Summary", result,
                    file_name="executive_summary.md", use_container_width=True)
            except Exception as e:
                st.error(f"❌ {e}")


# ══════════════════════════════════════════════════════════════
#           DASHBOARD 2: FINANCIAL INTELLIGENCE
# ══════════════════════════════════════════════════════════════

elif dashboard == "💰 Financial Intelligence":

    fin_df = generate_financial_data()

    st.markdown("## 💰 Financial Intelligence Dashboard")

    # KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("💵 Total Revenue",  f"${fin_df['Revenue'].sum():,.0f}")
    k2.metric("💰 Total Profit",   f"${fin_df['Profit'].sum():,.0f}")
    k3.metric("📊 Avg Margin",     f"{fin_df['Margin %'].mean():.1f}%")
    k4.metric("👥 Avg Customers",  f"{fin_df['Customers'].mean():.0f}")
    k5.metric("📉 Avg Churn",      f"{fin_df['Churn %'].mean():.1f}%")

    st.markdown("---")

    tabs = st.tabs([
        "📈 Revenue",
        "💰 Profitability",
        "👥 Customer Metrics",
        "🔮 Forecast",
        "📊 Full Table",
        "🤖 CFO Report",
    ])

    # Tab 1: Revenue
    with tabs[0]:
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Revenue Trend", "Revenue vs Costs", "Monthly Growth %", "Revenue Distribution"),
        )

        # Revenue trend
        fig.add_trace(go.Scatter(
            x=fin_df["Month"], y=fin_df["Revenue"],
            mode="lines+markers", name="Revenue",
            line=dict(color="#00d2ff", width=3),
            fill="tozeroy", fillcolor="rgba(0,210,255,0.1)"
        ), row=1, col=1)

        # Revenue vs Costs
        fig.add_trace(go.Bar(x=fin_df["Month"], y=fin_df["Revenue"],
                             name="Revenue", marker_color="#00d2ff"), row=1, col=2)
        fig.add_trace(go.Bar(x=fin_df["Month"], y=fin_df["Costs"],
                             name="Costs", marker_color="#ff6b6b"), row=1, col=2)

        # Growth %
        growth = fin_df["Revenue"].pct_change() * 100
        colors = ["#4ade80" if g > 0 else "#f87171" for g in growth]
        fig.add_trace(go.Bar(
            x=fin_df["Month"], y=growth,
            name="Growth %", marker_color=colors,
        ), row=2, col=1)

        # Distribution
        fig.add_trace(go.Box(
            y=fin_df["Revenue"], name="Revenue Range",
            marker_color="#7b2ff7",
        ), row=2, col=2)

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="#050510",
            paper_bgcolor="#050510",
            height=700, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Profitability
    with tabs[1]:
        col1, col2 = st.columns(2)

        with col1:
            # Profit waterfall
            fig_wf = go.Figure(go.Waterfall(
                name="Waterfall",
                orientation="v",
                measure=["relative"] * len(fin_df),
                x=fin_df["Month"],
                y=fin_df["Profit"].diff().fillna(fin_df["Profit"].iloc[0]).astype(int),
                connector={"line": {"color": "rgb(63,63,63)"}},
                increasing={"marker": {"color": "#4ade80"}},
                decreasing={"marker": {"color": "#f87171"}},
            ))
            fig_wf.update_layout(
                title="Profit Waterfall",
                template="plotly_dark",
                plot_bgcolor="#050510", paper_bgcolor="#0d0d1a",
                height=400,
            )
            st.plotly_chart(fig_wf, use_container_width=True)

        with col2:
            # Margin gauge
            avg_margin = fin_df["Margin %"].mean()
            fig_gauge = go.Figure(go.Indicator(
                mode  = "gauge+number+delta",
                value = avg_margin,
                delta = {"reference": 30},
                gauge = {
                    "axis"  : {"range": [0, 60]},
                    "bar"   : {"color": "#7b2ff7"},
                    "steps" : [
                        {"range": [0, 20],  "color": "#1a1a2e"},
                        {"range": [20, 40], "color": "#2a2a4e"},
                        {"range": [40, 60], "color": "#3a3a6e"},
                    ],
                    "threshold": {
                        "line" : {"color": "#00d2ff", "width": 4},
                        "thickness": 0.75,
                        "value": 35,
                    }
                },
                title = {"text": "Avg Profit Margin %"},
            ))
            fig_gauge.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0d0d1a", height=400,
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        # Margin trend area
        fig_margin = px.area(
            fin_df, x="Month", y="Margin %",
            title="Profit Margin Trend",
            color_discrete_sequence=["#4ade80"],
            template="plotly_dark",
        )
        fig_margin.update_layout(
            plot_bgcolor="#050510", paper_bgcolor="#050510",
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    # Tab 3: Customer Metrics
    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            # Customers trend
            fig_cust = px.bar(
                fin_df, x="Month", y="Customers",
                title="Monthly Active Customers",
                color="Customers",
                color_continuous_scale="Blues",
                template="plotly_dark",
            )
            fig_cust.update_layout(
                plot_bgcolor="#050510", paper_bgcolor="#0d0d1a",
            )
            st.plotly_chart(fig_cust, use_container_width=True)

            # Churn
            fig_churn = px.line(
                fin_df, x="Month", y="Churn %",
                title="Monthly Churn Rate %",
                color_discrete_sequence=["#f87171"],
                template="plotly_dark",
            )
            fig_churn.update_layout(
                plot_bgcolor="#050510", paper_bgcolor="#0d0d1a",
            )
            st.plotly_chart(fig_churn, use_container_width=True)

        with col2:
            # LTV vs CAC scatter
            fig_scatter = px.scatter(
                fin_df, x="CAC", y="LTV",
                size="Revenue", color="Margin %",
                title="LTV vs CAC Analysis",
                color_continuous_scale="Viridis",
                template="plotly_dark",
                hover_data=["Month"],
            )
            fig_scatter.update_layout(
                plot_bgcolor="#050510", paper_bgcolor="#0d0d1a",
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            # LTV/CAC ratio
            fin_df["LTV/CAC"] = (fin_df["LTV"] / fin_df["CAC"]).round(2)
            fig_ratio = px.line(
                fin_df, x="Month", y="LTV/CAC",
                title="LTV/CAC Ratio (>3 = Healthy)",
                color_discrete_sequence=["#4ade80"],
                template="plotly_dark",
            )
            fig_ratio.add_hline(y=3, line_dash="dash",
                                line_color="#ff6b6b",
                                annotation_text="Min Healthy = 3x")
            fig_ratio.update_layout(
                plot_bgcolor="#050510", paper_bgcolor="#0d0d1a",
            )
            st.plotly_chart(fig_ratio, use_container_width=True)

    # Tab 4: Forecast
    with tabs[3]:
        st.markdown("### 🔮 Revenue Forecast (Next 6 Months)")

        # Simple linear forecast
        from numpy.polynomial import polynomial as P
        x = np.arange(len(fin_df))
        y = fin_df["Revenue"].values
        coef = P.polyfit(x, y, 2)

        future_x    = np.arange(len(fin_df), len(fin_df) + 6)
        future_rev  = P.polyval(future_x, coef).astype(int)
        future_months = pd.date_range(
            start=pd.to_datetime(fin_df["Month"].iloc[-1], format="%b %Y") + timedelta(days=32),
            periods=6, freq="MS"
        ).strftime("%b %Y")

        forecast_df = pd.DataFrame({
            "Month"    : list(fin_df["Month"]) + list(future_months),
            "Revenue"  : list(fin_df["Revenue"]) + list(future_rev),
            "Type"     : ["Actual"] * len(fin_df) + ["Forecast"] * 6,
        })

        fig_forecast = px.line(
            forecast_df, x="Month", y="Revenue",
            color="Type", title="Revenue Forecast",
            color_discrete_map={"Actual": "#00d2ff", "Forecast": "#fbbf24"},
            template="plotly_dark",
        )
        fig_forecast.update_layout(
            plot_bgcolor="#050510", paper_bgcolor="#050510",
        )
        st.plotly_chart(fig_forecast, use_container_width=True)

        # Forecast table
        st.markdown("### 📋 Forecast Table")
        forecast_table = pd.DataFrame({
            "Month"            : future_months,
            "Forecast Revenue" : [f"${r:,.0f}" for r in future_rev],
            "Scenario (Best)"  : [f"${r*1.15:,.0f}" for r in future_rev],
            "Scenario (Base)"  : [f"${r:,.0f}" for r in future_rev],
            "Scenario (Worst)" : [f"${r*0.85:,.0f}" for r in future_rev],
        })
        st.dataframe(forecast_table, use_container_width=True)

    # Tab 5: Full Table
    with tabs[4]:
        st.markdown("### 📊 Full Financial Data")
        styled_df = fin_df.copy()
        styled_df["Revenue"] = styled_df["Revenue"].apply(lambda x: f"${x:,.0f}")
        styled_df["Costs"]   = styled_df["Costs"].apply(lambda x: f"${x:,.0f}")
        styled_df["Profit"]  = styled_df["Profit"].apply(lambda x: f"${x:,.0f}")
        st.dataframe(styled_df, use_container_width=True)

        csv = fin_df.to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv,
            file_name="financial_data.csv", use_container_width=True)

    # Tab 6: CFO Report
    with tabs[5]:
        st.markdown("### 🤖 AI CFO Report")
        if st.button("💰 Generate CFO Report", use_container_width=True):
            context = (
                f"Revenue: ${fin_df['Revenue'].iloc[-1]:,.0f} (latest month)\n"
                f"Total Revenue YTD: ${fin_df['Revenue'].sum():,.0f}\n"
                f"Total Profit YTD: ${fin_df['Profit'].sum():,.0f}\n"
                f"Avg Margin: {fin_df['Margin %'].mean():.1f}%\n"
                f"Avg Customers: {fin_df['Customers'].mean():.0f}\n"
                f"Avg Churn: {fin_df['Churn %'].mean():.1f}%\n"
                f"Avg LTV: ${fin_df['LTV'].mean():,.0f}\n"
                f"Avg CAC: ${fin_df['CAC'].mean():,.0f}\n"
                f"LTV/CAC Ratio: {(fin_df['LTV']/fin_df['CAC']).mean():.1f}x"
            )
            with st.spinner("💰 CFO analyst working..."):
                try:
                    crew   = CFOReportCrew(financial_context=context, company="Dashboard")
                    result = crew.run()
                    st.markdown(result)
                    path   = OUTPUTS_DIR / f"cfo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    path.write_text(result, encoding="utf-8")
                    st.download_button("⬇️ Download CFO Report", result,
                        file_name="cfo_report.md", use_container_width=True)
                except Exception as e:
                    st.error(f"❌ {e}")


# ══════════════════════════════════════════════════════════════
#           DASHBOARD 3: HR ANALYTICS
# ══════════════════════════════════════════════════════════════

elif dashboard == "👥 HR Analytics":

    hr_df = generate_hr_data()

    st.markdown("## 👥 HR Analytics Dashboard")

    # KPIs
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("👥 Total",        f"{len(hr_df)}")
    k2.metric("💵 Avg Salary",   f"${hr_df['Salary'].mean():,.0f}")
    k3.metric("⭐ Avg Perf",     f"{hr_df['Performance'].mean():.1f}")
    k4.metric("😊 Satisfaction", f"{hr_df['Satisfaction'].mean():.1f}/5")
    k5.metric("📅 Avg Tenure",   f"{hr_df['Tenure (yrs)'].mean():.1f} yrs")
    k6.metric("⚠️ High Risk",    f"{(hr_df['Attrition Risk']=='High').sum()}")

    st.markdown("---")

    tabs = st.tabs([
        "👥 Workforce",
        "💵 Compensation",
        "⭐ Performance",
        "⚠️ Attrition Risk",
        "📊 Diversity",
        "🔍 Deep Search",
    ])

    # Tab 1: Workforce
    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            # Dept distribution
            dept_df = hr_df["Department"].value_counts().reset_index()
            dept_df.columns = ["Department", "Count"]
            fig = px.bar(dept_df, x="Count", y="Department",
                        orientation="h", title="Headcount by Department",
                        color="Count", color_continuous_scale="Viridis",
                        template="plotly_dark")
            fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

            # Level distribution
            level_df = hr_df["Level"].value_counts().reset_index()
            level_df.columns = ["Level", "Count"]
            fig2 = px.pie(level_df, values="Count", names="Level",
                         title="Distribution by Level", hole=0.4,
                         template="plotly_dark")
            fig2.update_layout(paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # Age distribution
            fig3 = px.histogram(hr_df, x="Age", nbins=20,
                               title="Age Distribution",
                               color_discrete_sequence=["#7b2ff7"],
                               template="plotly_dark")
            fig3.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig3, use_container_width=True)

            # Remote work
            remote_df = hr_df["Remote"].value_counts().reset_index()
            remote_df.columns = ["Remote", "Count"]
            fig4 = px.pie(remote_df, values="Count", names="Remote",
                         title="Remote Work Distribution", hole=0.4,
                         color_discrete_sequence=["#00d2ff", "#7b2ff7", "#4ade80"],
                         template="plotly_dark")
            fig4.update_layout(paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig4, use_container_width=True)

    # Tab 2: Compensation
    with tabs[1]:
        col1, col2 = st.columns(2)

        with col1:
            # Salary by dept
            sal_dept = hr_df.groupby("Department")["Salary"].mean().reset_index()
            sal_dept.columns = ["Department", "Avg Salary"]
            fig = px.bar(sal_dept, x="Department", y="Avg Salary",
                        title="Avg Salary by Department",
                        color="Avg Salary", color_continuous_scale="Blues",
                        template="plotly_dark")
            fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Salary by level
            sal_level = hr_df.groupby("Level")["Salary"].mean().sort_values().reset_index()
            fig2 = px.bar(sal_level, x="Salary", y="Level",
                         orientation="h", title="Avg Salary by Level",
                         color="Salary", color_continuous_scale="Viridis",
                         template="plotly_dark")
            fig2.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

        # Salary distribution
        fig3 = px.histogram(hr_df, x="Salary", nbins=30,
                           color="Department",
                           title="Salary Distribution by Department",
                           template="plotly_dark")
        fig3.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
        st.plotly_chart(fig3, use_container_width=True)

    # Tab 3: Performance
    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            # Performance vs Salary
            fig = px.scatter(hr_df, x="Performance", y="Salary",
                            color="Department", size="Training hrs",
                            title="Performance vs Salary",
                            template="plotly_dark",
                            hover_data=["Level", "Tenure (yrs)"])
            fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Performance by dept
            perf_dept = hr_df.groupby("Department")["Performance"].mean().reset_index()
            fig2 = px.bar(perf_dept, x="Department", y="Performance",
                         title="Avg Performance by Department",
                         color="Performance",
                         color_continuous_scale="RdYlGn",
                         template="plotly_dark")
            fig2.add_hline(y=3.5, line_dash="dash",
                          line_color="#fbbf24",
                          annotation_text="Target: 3.5")
            fig2.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

        # Satisfaction vs Performance
        fig3 = px.scatter(hr_df, x="Satisfaction", y="Performance",
                         color="Attrition Risk",
                         color_discrete_map={
                             "Low": "#4ade80",
                             "Medium": "#fbbf24",
                             "High": "#f87171"
                         },
                         title="Satisfaction vs Performance (Attrition Risk)",
                         template="plotly_dark",
                         size="Salary")
        fig3.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
        st.plotly_chart(fig3, use_container_width=True)

    # Tab 4: Attrition Risk
    with tabs[3]:
        # Risk summary
        risk_counts = hr_df["Attrition Risk"].value_counts()
        r1, r2, r3 = st.columns(3)
        r1.metric("🟢 Low Risk",    f"{risk_counts.get('Low', 0)}")
        r2.metric("🟡 Medium Risk", f"{risk_counts.get('Medium', 0)}")
        r3.metric("🔴 High Risk",   f"{risk_counts.get('High', 0)}")

        col1, col2 = st.columns(2)
        with col1:
            # Risk by dept
            risk_dept = hr_df.groupby(["Department", "Attrition Risk"]).size().reset_index(name="Count")
            fig = px.bar(risk_dept, x="Department", y="Count",
                        color="Attrition Risk",
                        color_discrete_map={
                            "Low": "#4ade80",
                            "Medium": "#fbbf24",
                            "High": "#f87171"
                        },
                        title="Attrition Risk by Department",
                        template="plotly_dark", barmode="stack")
            fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # High risk employees
            high_risk = hr_df[hr_df["Attrition Risk"] == "High"][
                ["Department", "Level", "Salary", "Performance", "Satisfaction", "Tenure (yrs)"]
            ].head(10)
            st.markdown("### 🔴 High Risk Employees")
            st.dataframe(high_risk, use_container_width=True)

        # Tenure vs Attrition
        fig2 = px.box(hr_df, x="Attrition Risk", y="Tenure (yrs)",
                     color="Attrition Risk",
                     color_discrete_map={
                         "Low": "#4ade80",
                         "Medium": "#fbbf24",
                         "High": "#f87171"
                     },
                     title="Tenure Distribution by Attrition Risk",
                     template="plotly_dark")
        fig2.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
        st.plotly_chart(fig2, use_container_width=True)

    # Tab 5: Diversity
    with tabs[4]:
        col1, col2, col3 = st.columns(3)

        with col1:
            gender_df = hr_df["Gender"].value_counts().reset_index()
            gender_df.columns = ["Gender", "Count"]
            fig = px.pie(gender_df, values="Count", names="Gender",
                        title="Gender Distribution", hole=0.4,
                        color_discrete_sequence=["#00d2ff", "#ff6b6b", "#4ade80"],
                        template="plotly_dark")
            fig.update_layout(paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            remote_df = hr_df["Remote"].value_counts().reset_index()
            remote_df.columns = ["Remote", "Count"]
            fig2 = px.pie(remote_df, values="Count", names="Remote",
                         title="Remote Work", hole=0.4,
                         template="plotly_dark")
            fig2.update_layout(paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            level_df = hr_df["Level"].value_counts().reset_index()
            level_df.columns = ["Level", "Count"]
            fig3 = px.pie(level_df, values="Count", names="Level",
                         title="Level Distribution", hole=0.4,
                         template="plotly_dark")
            fig3.update_layout(paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig3, use_container_width=True)

        # Salary equity
        sal_gender = hr_df.groupby(["Gender", "Department"])["Salary"].mean().reset_index()
        fig4 = px.bar(sal_gender, x="Department", y="Salary",
                     color="Gender", barmode="group",
                     title="Salary Equity: Gender by Department",
                     template="plotly_dark")
        fig4.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
        st.plotly_chart(fig4, use_container_width=True)

    # Tab 6: Deep Search
    with tabs[5]:
        st.markdown("### 🔍 Employee Deep Search & Filter")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            dept_filter = st.multiselect("Department",
                hr_df["Department"].unique().tolist(), default=[])
        with c2:
            level_filter = st.multiselect("Level",
                hr_df["Level"].unique().tolist(), default=[])
        with c3:
            risk_filter = st.multiselect("Attrition Risk",
                ["Low", "Medium", "High"], default=[])
        with c4:
            perf_min = st.slider("Min Performance", 2.5, 5.0, 3.0, 0.1)

        filtered = hr_df.copy()
        if dept_filter:
            filtered = filtered[filtered["Department"].isin(dept_filter)]
        if level_filter:
            filtered = filtered[filtered["Level"].isin(level_filter)]
        if risk_filter:
            filtered = filtered[filtered["Attrition Risk"].isin(risk_filter)]
        filtered = filtered[filtered["Performance"] >= perf_min]

        st.info(f"Showing {len(filtered)} employees")
        st.dataframe(filtered, use_container_width=True)

        csv = filtered.to_csv(index=False)
        st.download_button("⬇️ Export Filtered Data", csv,
            file_name="hr_filtered.csv", use_container_width=True)


# ══════════════════════════════════════════════════════════════
#           DASHBOARD 4: SALES INTELLIGENCE
# ══════════════════════════════════════════════════════════════

elif dashboard == "📈 Sales Intelligence":

    sales_df = generate_sales_data()

    st.markdown("## 📈 Sales Intelligence Dashboard")

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("💵 Total Revenue",  f"${sales_df['Revenue'].sum():,.0f}")
    k2.metric("📦 Total Units",    f"{sales_df['Units'].sum():,}")
    k3.metric("💰 Total Profit",   f"${sales_df['Profit'].sum():,.0f}")
    k4.metric("🎯 Total Leads",    f"{sales_df['Leads'].sum():,}")
    k5.metric("✅ Converted",      f"{sales_df['Converted'].sum():,}")

    st.markdown("---")

    tabs = st.tabs([
        "📈 Revenue",
        "🗺️ Regional",
        "📦 Products",
        "🎯 Conversion",
        "📊 Raw Data",
    ])

    # Tab 1: Revenue
    with tabs[0]:
        sales_daily = sales_df.groupby("Date")["Revenue"].sum().reset_index()
        fig = px.area(sales_daily, x="Date", y="Revenue",
                     title="Daily Revenue Trend",
                     color_discrete_sequence=["#00d2ff"],
                     template="plotly_dark")
        fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            ch_rev = sales_df.groupby("Channel")["Revenue"].sum().reset_index()
            fig2 = px.pie(ch_rev, values="Revenue", names="Channel",
                         title="Revenue by Channel", hole=0.4,
                         template="plotly_dark")
            fig2.update_layout(paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            disc_rev = sales_df.copy()
            disc_rev["Discount Band"] = pd.cut(
                disc_rev["Discount %"],
                bins=[0, 5, 10, 20, 30],
                labels=["0-5%", "5-10%", "10-20%", "20-30%"]
            )
            disc_summary = disc_rev.groupby("Discount Band")["Revenue"].mean().reset_index()
            fig3 = px.bar(disc_summary, x="Discount Band", y="Revenue",
                         title="Avg Revenue by Discount Band",
                         color="Revenue",
                         color_continuous_scale="RdYlGn_r",
                         template="plotly_dark")
            fig3.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig3, use_container_width=True)

    # Tab 2: Regional
    with tabs[1]:
        reg_df = sales_df.groupby("Region").agg({
            "Revenue": "sum", "Profit": "sum",
            "Units": "sum", "Leads": "sum"
        }).reset_index()

        fig = px.bar(reg_df, x="Region", y="Revenue",
                    color="Profit", title="Revenue & Profit by Region",
                    color_continuous_scale="Viridis",
                    template="plotly_dark")
        fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
        st.plotly_chart(fig, use_container_width=True)

        # Regional heatmap
        reg_prod = sales_df.groupby(["Region", "Product"])["Revenue"].sum().reset_index()
        fig2 = px.density_heatmap(reg_prod, x="Region", y="Product", z="Revenue",
                                  title="Revenue Heatmap: Region × Product",
                                  color_continuous_scale="Viridis",
                                  template="plotly_dark")
        fig2.update_layout(paper_bgcolor="#050510")
        st.plotly_chart(fig2, use_container_width=True)

    # Tab 3: Products
    with tabs[2]:
        prod_df = sales_df.groupby("Product").agg({
            "Revenue": "sum", "Profit": "sum",
            "Units": "sum",
        }).reset_index()
        prod_df["Margin %"] = (prod_df["Profit"] / prod_df["Revenue"] * 100).round(1)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(prod_df, x="Product", y="Revenue",
                        title="Revenue by Product",
                        color="Margin %",
                        color_continuous_scale="RdYlGn",
                        template="plotly_dark")
            fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.scatter(prod_df, x="Units", y="Revenue",
                             size="Profit", color="Margin %",
                             text="Product",
                             title="Units vs Revenue (Bubble = Profit)",
                             color_continuous_scale="Viridis",
                             template="plotly_dark")
            fig2.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

    # Tab 4: Conversion
    with tabs[3]:
        sales_df["Conv Rate %"] = (sales_df["Converted"] / sales_df["Leads"] * 100).round(1)

        col1, col2 = st.columns(2)
        with col1:
            conv_ch = sales_df.groupby("Channel")["Conv Rate %"].mean().reset_index()
            fig = px.bar(conv_ch, x="Channel", y="Conv Rate %",
                        title="Conversion Rate by Channel",
                        color="Conv Rate %",
                        color_continuous_scale="RdYlGn",
                        template="plotly_dark")
            fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            conv_reg = sales_df.groupby("Region")["Conv Rate %"].mean().reset_index()
            fig2 = px.bar(conv_reg, x="Region", y="Conv Rate %",
                         title="Conversion Rate by Region",
                         color="Conv Rate %",
                         color_continuous_scale="Blues",
                         template="plotly_dark")
            fig2.update_layout(plot_bgcolor="#050510", paper_bgcolor="#0d0d1a")
            st.plotly_chart(fig2, use_container_width=True)

        # Leads funnel
        total_leads  = int(sales_df["Leads"].sum())
        total_conv   = int(sales_df["Converted"].sum())
        fig3 = go.Figure(go.Funnel(
            y=["Total Leads", "Contacted", "Qualified", "Proposal", "Converted"],
            x=[total_leads,
               int(total_leads * 0.7),
               int(total_leads * 0.45),
               int(total_leads * 0.25),
               total_conv],
            textinfo="value+percent initial",
            marker={"color": ["#00d2ff", "#7b2ff7", "#4ade80", "#fbbf24", "#f87171"]},
        ))
        fig3.update_layout(
            title="Sales Funnel",
            template="plotly_dark",
            paper_bgcolor="#050510",
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Tab 5: Raw Data
    with tabs[4]:
        st.dataframe(sales_df, use_container_width=True)
        csv = sales_df.to_csv(index=False)
        st.download_button("⬇️ Export Sales Data", csv,
            file_name="sales_data.csv", use_container_width=True)


# ══════════════════════════════════════════════════════════════
#           DASHBOARD 5: CUSTOM DATA UPLOAD
# ══════════════════════════════════════════════════════════════

elif dashboard == "📊 Custom Data Upload":

    st.markdown("## 📊 Custom Data Analytics")

    uploaded = st.file_uploader(
        "📁 Upload Your Dataset",
        type=["csv", "xlsx", "xls"],
        help="CSV or Excel — Max 50MB"
    )

    if uploaded:
        save_path = UPLOADS_DIR / uploaded.name
        save_path.write_bytes(uploaded.getvalue())

        try:
            df = pd.read_csv(save_path) if uploaded.name.endswith(".csv") else pd.read_excel(save_path)
            st.success(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

            # KPIs
            if num_cols:
                cols = st.columns(min(4, len(num_cols)))
                for i, col in enumerate(num_cols[:4]):
                    cols[i].metric(f"Σ {col}", f"{df[col].sum():,.1f}")

            st.markdown("---")

            tabs = st.tabs(["👀 Preview", "📊 Charts", "📈 Trends", "🔍 Stats", "🤖 AI"])

            with tabs[0]:
                n = st.slider("Rows", 5, min(100, len(df)), 20)
                st.dataframe(df.head(n), use_container_width=True)

            with tabs[1]:
                if num_cols and cat_cols:
                    c1, c2 = st.columns(2)
                    with c1:
                        x = st.selectbox("X Axis (Category)", cat_cols)
                    with c2:
                        y = st.selectbox("Y Axis (Number)", num_cols)

                    chart_type = st.radio("Chart Type", ["Bar", "Box", "Violin", "Strip"], horizontal=True)

                    if chart_type == "Bar":
                        fig = px.bar(df, x=x, y=y, color=x,
                                    template="plotly_dark",
                                    title=f"{y} by {x}")
                    elif chart_type == "Box":
                        fig = px.box(df, x=x, y=y, color=x,
                                    template="plotly_dark",
                                    title=f"{y} by {x}")
                    elif chart_type == "Violin":
                        fig = px.violin(df, x=x, y=y, color=x,
                                       template="plotly_dark",
                                       title=f"{y} by {x}")
                    else:
                        fig = px.strip(df, x=x, y=y, color=x,
                                      template="plotly_dark",
                                      title=f"{y} by {x}")

                    fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
                    st.plotly_chart(fig, use_container_width=True)

            with tabs[2]:
                if len(num_cols) >= 2:
                    c1, c2 = st.columns(2)
                    with c1:
                        x_t = st.selectbox("X Axis", df.columns.tolist(), key="tx")
                    with c2:
                        y_t = st.selectbox("Y Axis", num_cols, key="ty")

                    fig = px.line(df, x=x_t, y=y_t,
                                 title=f"{y_t} over {x_t}",
                                 template="plotly_dark",
                                 color_discrete_sequence=["#00d2ff"])
                    fig.update_layout(plot_bgcolor="#050510", paper_bgcolor="#050510")
                    st.plotly_chart(fig, use_container_width=True)

                # Correlation
                if len(num_cols) >= 2:
                    corr = df[num_cols].corr()
                    fig2 = px.imshow(corr, title="Correlation Matrix",
                                    color_continuous_scale="RdBu_r",
                                    template="plotly_dark")
                    fig2.update_layout(paper_bgcolor="#050510")
                    st.plotly_chart(fig2, use_container_width=True)

            with tabs[3]:
                st.dataframe(df.describe().round(2), use_container_width=True)

                miss = df.isnull().sum()
                miss = miss[miss > 0]
                if not miss.empty:
                    st.warning(f"⚠️ Missing values in {len(miss)} columns")
                    st.dataframe(miss.reset_index().rename(
                        columns={"index": "Column", 0: "Missing"}),
                        use_container_width=True
                    )
                else:
                    st.success("✅ No missing values!")

            with tabs[4]:
                if st.button("🤖 Generate AI Insights", use_container_width=True):
                    context = (
                        f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns\n"
                        f"Numeric columns: {num_cols}\n"
                        f"Categorical: {cat_cols}\n"
                        f"Stats:\n{df[num_cols].describe().round(2).to_string() if num_cols else 'N/A'}"
                    )
                    with st.spinner("🤖 AI analyzing..."):
                        try:
                            crew   = CEOReportCrew(context=context, company="Data Analysis")
                            result = crew.run()
                            st.markdown(result)
                            path   = OUTPUTS_DIR / f"custom_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                            path.write_text(result, encoding="utf-8")
                            st.download_button("⬇️ Download Insights", result,
                                file_name="insights.md", use_container_width=True)
                        except Exception as e:
                            st.error(f"❌ {e}")

        except Exception as e:
            st.error(f"❌ {e}")

    else:
        # Sample data option
        st.info("📁 Upload your CSV/Excel file above")
        st.markdown("### 💡 Or use sample data:")
        if st.button("📊 Load Financial Sample", use_container_width=True):
            df = generate_financial_data()
            st.dataframe(df.head(), use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Sample CSV", csv,
                file_name="sample_financial.csv", use_container_width=True)


# ══════════════════════════════════════════════════════════════
#           DASHBOARD 6: AI REPORT GENERATOR
# ══════════════════════════════════════════════════════════════

elif dashboard == "🤖 AI Report Generator":

    st.markdown("## 🤖 AI Report Generator")

    report_type = st.selectbox("Report Type", [
        "👔 CEO Strategic Report",
        "💰 CFO Financial Report",
        "📊 Business Analytics Report",
        "🎯 Market Intelligence Report",
    ])

    context = st.text_area(
        "📋 Business Context",
        placeholder="Describe your business situation, metrics, challenges...",
        height=200,
    )

    file_upload = st.file_uploader("📎 Attach Data (Optional)", type=["csv", "txt", "md"])

    if file_upload:
        try:
            if file_upload.name.endswith(".csv"):
                df = pd.read_csv(file_upload)
                context += f"\n\nData Preview:\n{df.head(10).to_string()}"
            else:
                context += f"\n\n{file_upload.read().decode('utf-8')[:2000]}"
            st.success(f"✅ File attached: {file_upload.name}")
        except Exception:
            pass

    if st.button(f"🤖 Generate {report_type}", use_container_width=True) and context:
        with st.spinner(f"🤖 Generating {report_type}..."):
            try:
                if "CEO" in report_type:
                    crew = CEOReportCrew(context=context, company="Business")
                else:
                    crew = CFOReportCrew(financial_context=context, company="Business")

                result = crew.run()
                st.success("✅ Report Ready!")
                st.markdown("---")
                st.markdown(result)

                path = OUTPUTS_DIR / f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                path.write_text(result, encoding="utf-8")

                st.download_button(
                    "⬇️ Download Report",
                    data      = result,
                    file_name = f"report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime      = "text/markdown",
                    use_container_width = True,
                )
            except Exception as e:
                st.error(f"❌ {e}")


# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.markdown("**📊 Executive Deep Dashboard v1.0**")
c2.markdown("LangGraph + CrewAI + Groq + Plotly")
c3.markdown(f"*{datetime.now().strftime('%B %d, %Y')}*")