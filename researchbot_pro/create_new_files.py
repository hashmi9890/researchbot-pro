"""
Creates all 11 missing files for Pro Upgrade
Run once → Delete this file after
"""

import os

files = {}

# ══════════════════════════════════════
#  src/analytics/__init__.py
# ══════════════════════════════════════

files["src/analytics/__init__.py"] = '''from .data_loader import DataLoader
from .charts import ChartEngine

__all__ = ["DataLoader", "ChartEngine"]
'''

# ══════════════════════════════════════
#  src/analytics/data_loader.py
# ══════════════════════════════════════

files["src/analytics/data_loader.py"] = '''"""
Data Loader — CSV / Excel files load + profiling
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataLoader:

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.df = None

    def load(self) -> pd.DataFrame:
        suffix = self.file_path.suffix.lower()
        if suffix == ".csv":
            self.df = pd.read_csv(self.file_path)
        elif suffix in [".xlsx", ".xls"]:
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file: {suffix}")
        return self.df

    def profile(self) -> dict:
        if self.df is None:
            self.load()
        df = self.df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        profile = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "numeric_cols": numeric_cols,
            "categorical_cols": df.select_dtypes(include=["object"]).columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "duplicates": int(df.duplicated().sum()),
        }
        if numeric_cols:
            profile["summary_stats"] = df[numeric_cols].describe().round(2).to_dict()
        return profile

    def get_kpis(self) -> dict:
        if self.df is None:
            self.load()
        df = self.df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        kpis = {}
        for col in numeric_cols:
            kpis[col] = {
                "total": round(float(df[col].sum()), 2),
                "mean": round(float(df[col].mean()), 2),
                "median": round(float(df[col].median()), 2),
                "max": round(float(df[col].max()), 2),
                "min": round(float(df[col].min()), 2),
                "std": round(float(df[col].std()), 2),
            }
        return kpis
'''

# ══════════════════════════════════════
#  src/analytics/charts.py
# ══════════════════════════════════════

files["src/analytics/charts.py"] = '''"""
Chart Engine — Plotly professional charts
"""

import plotly.express as px
import pandas as pd
import numpy as np


class ChartEngine:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def correlation_heatmap(self):
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return None
        corr = numeric_df.corr().round(2)
        fig = px.imshow(
            corr, title="Correlation Heatmap",
            color_continuous_scale="RdBu_r", aspect="auto",
        )
        return fig

    def missing_values_chart(self):
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if missing.empty:
            return None
        fig = px.bar(
            x=missing.index, y=missing.values,
            title="Missing Values by Column",
            labels={"x": "Column", "y": "Missing Count"},
            color=missing.values, color_continuous_scale="Reds",
        )
        return fig

    def distribution_chart(self, column: str):
        if column not in self.df.columns:
            return None
        if self.df[column].dtype in [np.float64, np.int64]:
            fig = px.histogram(
                self.df, x=column, title=f"Distribution: {column}",
                nbins=30, color_discrete_sequence=["#7b2ff7"],
            )
        else:
            counts = self.df[column].value_counts().head(20)
            fig = px.bar(
                x=counts.index, y=counts.values,
                title=f"Top Values: {column}",
                labels={"x": column, "y": "Count"},
                color_discrete_sequence=["#00d2ff"],
            )
        return fig

    def trend_chart(self, x_col: str, y_col: str):
        if x_col not in self.df.columns or y_col not in self.df.columns:
            return None
        fig = px.line(
            self.df, x=x_col, y=y_col,
            title=f"Trend: {y_col} over {x_col}",
            color_discrete_sequence=["#00d2ff"],
        )
        return fig

    def kpi_summary_chart(self, numeric_cols: list):
        if not numeric_cols:
            return None
        means = self.df[numeric_cols].mean().round(2)
        fig = px.bar(
            x=means.index, y=means.values, title="KPI Averages",
            labels={"x": "Metric", "y": "Average Value"},
            color=means.values, color_continuous_scale="Viridis",
        )
        return fig
'''

# ══════════════════════════════════════
#  src/prompts/__init__.py
# ══════════════════════════════════════

files["src/prompts/__init__.py"] = '''from .templates import PromptTemplates
__all__ = ["PromptTemplates"]
'''

# ══════════════════════════════════════
#  src/prompts/templates.py
# ══════════════════════════════════════

files["src/prompts/templates.py"] = '''"""
Prompt Templates — Professional prompt patterns
"""


class PromptTemplates:

    @staticmethod
    def ceo_system() -> str:
        return (
            "You are a world-class CEO and strategic advisor. "
            "You communicate with clarity, precision, and urgency. "
            "Every output is decision-ready. No fluff."
        )

    @staticmethod
    def cfo_system() -> str:
        return (
            "You are an elite CFO with deep expertise in financial "
            "modeling, unit economics, and capital efficiency. "
            "You translate numbers into strategic narratives."
        )

    @staticmethod
    def problem_solver_system() -> str:
        return (
            "You are a senior management consultant. "
            "You use frameworks like 5-Why, MECE, First Principles. "
            "Every recommendation is specific, measurable, executable."
        )

    @staticmethod
    def analysis_templates() -> dict:
        return {
            "CEO Report": (
                "Write a CEO strategic report covering: "
                "Executive Summary, Situation, Opportunities, Risks, "
                "Priorities, Decisions Needed, 30/60/90 Day Plan, KPIs"
            ),
            "CFO Report": (
                "Write a CFO financial report covering: "
                "Revenue, Costs, Margins, Burn, Runway, "
                "Unit Economics, Risks, Recommendations"
            ),
            "Problem Solving": (
                "Solve this business problem using: "
                "Root Cause Analysis, 3 Solution Options, "
                "Recommended Plan, 30/60/90 Day Roadmap, KPIs"
            ),
            "Data Analysis": (
                "Analyze this data and provide: "
                "Key Insights, Trends, Anomalies, "
                "KPI Summary, Action Recommendations"
            ),
            "Market Research": (
                "Research this topic and provide: "
                "Market Overview, Key Players, Trends, "
                "Opportunities, Risks, Strategic Recommendations"
            ),
        }
'''

# ══════════════════════════════════════
#  src/agents/problem_solver_agent.py
# ══════════════════════════════════════

files["src/agents/problem_solver_agent.py"] = '''"""
Problem Solver Agent — Root cause + solutions
"""

from crewai import Agent
from src.config import config


def create_problem_solver() -> Agent:
    return Agent(
        role="Senior Business Problem Solver & Strategy Consultant",
        goal=(
            "Analyze business problems deeply. Identify root causes, "
            "key blockers, and provide multiple solution options with "
            "a recommended 30/60/90 day execution plan."
        ),
        backstory=(
            "You are a McKinsey senior partner with 25 years experience "
            "solving complex business problems across 50+ industries. "
            "You use structured frameworks like 5-Why, MECE, First Principles. "
            "You never give vague advice."
        ),
        llm=config.MODEL_NAME,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )


def create_clarifier() -> Agent:
    return Agent(
        role="Problem Clarification Specialist",
        goal=(
            "Take a vague problem statement and clarify it into "
            "a structured, well-defined problem with clear scope, "
            "constraints, stakeholders, and success criteria."
        ),
        backstory=(
            "You are an expert in problem definition with a background "
            "in systems thinking and design thinking. You ask the right "
            "questions to eliminate ambiguity."
        ),
        llm=config.MODEL_NAME,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )


def create_risk_analyst() -> Agent:
    return Agent(
        role="Risk Assessment & Scenario Planning Analyst",
        goal=(
            "Identify all risks, failure modes, and edge cases "
            "in a proposed solution. Provide mitigation strategies "
            "and scenario plans (best/base/worst case)."
        ),
        backstory=(
            "You are a former hedge fund risk analyst turned startup advisor. "
            "You think adversarially — always asking what could go wrong. "
            "Your analysis is data-driven and probability-weighted."
        ),
        llm=config.MODEL_NAME,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )
'''

# ══════════════════════════════════════
#  src/agents/ceo_agent.py
# ══════════════════════════════════════

files["src/agents/ceo_agent.py"] = '''"""
CEO Report Agent — Executive strategic reports
"""

from crewai import Agent
from src.config import config


def create_ceo_agent() -> Agent:
    return Agent(
        role="Chief Executive Officer & Strategic Advisor",
        goal=(
            "Synthesize complex business information into "
            "clear, decision-ready CEO-level reports. Focus on "
            "strategic priorities, market opportunities, risks, "
            "and top-level KPIs. Write for a busy executive."
        ),
        backstory=(
            "You are a seasoned CEO who has led 3 unicorn startups "
            "and advised Fortune 500 companies. You communicate with "
            "brutal clarity — no fluff, no jargon."
        ),
        llm=config.MODEL_NAME,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )
'''

# ══════════════════════════════════════
#  src/agents/cfo_agent.py
# ══════════════════════════════════════

files["src/agents/cfo_agent.py"] = '''"""
CFO Report Agent — Financial analysis reports
"""

from crewai import Agent
from src.config import config


def create_cfo_agent() -> Agent:
    return Agent(
        role="Chief Financial Officer & Financial Strategy Advisor",
        goal=(
            "Analyze financial data and business metrics to produce "
            "clear CFO-level reports. Focus on revenue, costs, margins, "
            "burn rate, runway, unit economics, and financial risks."
        ),
        backstory=(
            "You are a CFO who has managed P&Ls from $1M to $500M. "
            "You have deep expertise in financial modeling. You translate "
            "numbers into stories and stories into action plans. "
            "You never hide bad news — you quantify it and solve it."
        ),
        llm=config.MODEL_NAME,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )
'''

# ══════════════════════════════════════
#  src/agents/prompt_agent.py
# ══════════════════════════════════════

files["src/agents/prompt_agent.py"] = '''"""
Prompt Engineering Agent — Optimize prompts
"""

from crewai import Agent
from src.config import config


def create_prompt_engineer() -> Agent:
    return Agent(
        role="Senior Prompt Engineer & LLM Optimization Specialist",
        goal=(
            "Analyze, improve, and optimize prompts for maximum "
            "LLM performance. Apply best practices: clear instructions, "
            "role assignment, output contracts, few-shot examples."
        ),
        backstory=(
            "You are one of the worlds leading prompt engineers. "
            "You understand token efficiency, context windows, "
            "hallucination prevention, and output consistency. "
            "You transform vague prompts into precision instruments."
        ),
        llm=config.MODEL_NAME,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )
'''

# ══════════════════════════════════════
#  src/crew/problem_crew.py
# ══════════════════════════════════════

files["src/crew/problem_crew.py"] = '''"""
Problem Solving Crew — Clarifier + Solver + Risk Analyst
"""

from crewai import Crew, Task, Process
from src.agents.problem_solver_agent import (
    create_clarifier,
    create_problem_solver,
    create_risk_analyst,
)


class ProblemSolvingCrew:

    def __init__(self, problem_data: dict) -> None:
        self.problem_data = problem_data
        self.clarifier = create_clarifier()
        self.solver = create_problem_solver()
        self.risk_analyst = create_risk_analyst()
        self._tasks = self._build_tasks()
        self._crew = Crew(
            agents=[self.clarifier, self.solver, self.risk_analyst],
            tasks=self._tasks,
            process=Process.sequential,
            verbose=True,
        )

    def _build_tasks(self) -> list:
        p = self.problem_data

        clarify_task = Task(
            description=(
                f"Clarify and structure this business problem:\\n\\n"
                f"Problem: {p.get('problem', 'N/A')}\\n"
                f"Industry: {p.get('industry', 'N/A')}\\n"
                f"Goal: {p.get('goal', 'N/A')}\\n"
                f"Constraints: {p.get('constraints', 'N/A')}\\n"
                f"Budget: {p.get('budget', 'N/A')}\\n"
                f"Timeline: {p.get('timeline', 'N/A')}\\n\\n"
                "DELIVERABLES:\\n"
                "1. Restated problem (clear, specific)\\n"
                "2. Root problem vs symptoms\\n"
                "3. Key stakeholders affected\\n"
                "4. Success criteria\\n"
                "5. Scope boundaries"
            ),
            expected_output="Structured problem definition with clear scope",
            agent=self.clarifier,
        )

        solve_task = Task(
            description=(
                "Based on the clarified problem, provide:\\n\\n"
                "1. Root Cause Analysis (5-Why method)\\n"
                "2. Key Blockers & Dependencies\\n"
                "3. Solution Option A (Low cost)\\n"
                "4. Solution Option B (Medium cost)\\n"
                "5. Solution Option C (High investment)\\n"
                "6. Recommended Solution with justification\\n"
                "7. 30-Day Action Plan\\n"
                "8. 60-Day Milestones\\n"
                "9. 90-Day Target State\\n"
                "10. KPIs to track success"
            ),
            expected_output="Complete problem solving report with 30/60/90 plan",
            agent=self.solver,
            context=[clarify_task],
        )

        risk_task = Task(
            description=(
                "Analyze the recommended solution and provide:\\n\\n"
                "1. Top 5 Risks (probability + impact)\\n"
                "2. Risk Mitigation Strategies\\n"
                "3. Best Case Scenario\\n"
                "4. Base Case Scenario\\n"
                "5. Worst Case Scenario\\n"
                "6. Contingency Plans\\n"
                "7. SWOT Analysis"
            ),
            expected_output="Risk and scenario analysis with SWOT",
            agent=self.risk_analyst,
            context=[clarify_task, solve_task],
        )

        return [clarify_task, solve_task, risk_task]

    def run(self) -> str:
        result = self._crew.kickoff(inputs=self.problem_data)
        return str(result)
'''

# ══════════════════════════════════════
#  src/crew/executive_crew.py
# ══════════════════════════════════════

files["src/crew/executive_crew.py"] = '''"""
Executive Crews — CEO, CFO, Prompt Engineering
"""

from crewai import Crew, Task, Process
from src.agents.researcher_agent import create_researcher
from src.agents.ceo_agent import create_ceo_agent
from src.agents.cfo_agent import create_cfo_agent
from src.agents.prompt_agent import create_prompt_engineer


class CEOReportCrew:

    def __init__(self, context: str, company: str = "Company") -> None:
        self.context = context
        self.company = company
        self.researcher = create_researcher()
        self.ceo_agent = create_ceo_agent()
        self._crew = Crew(
            agents=[self.researcher, self.ceo_agent],
            tasks=self._build_tasks(),
            process=Process.sequential,
            verbose=True,
        )

    def _build_tasks(self) -> list:
        research_task = Task(
            description=(
                f"Research and gather data about: {self.context}\\n"
                "Focus on: market position, competitors, opportunities, "
                "industry trends, and strategic landscape."
            ),
            expected_output="Comprehensive research with key insights",
            agent=self.researcher,
        )

        ceo_task = Task(
            description=(
                f"Write a CEO-level strategic report for {self.company}.\\n\\n"
                "REQUIRED SECTIONS:\\n"
                "# Executive Summary (3 bullets max)\\n"
                "## Situation Analysis\\n"
                "## Top 3 Strategic Opportunities\\n"
                "## Top 3 Critical Risks\\n"
                "## Recommended Strategic Priorities\\n"
                "## Decisions Required This Month\\n"
                "## 30/60/90 Day Action Plan\\n"
                "## KPI Dashboard (table format)\\n"
                "## Bottom Line\\n\\n"
                "Write for a busy CEO. Be direct. No fluff."
            ),
            expected_output="Professional CEO report with all sections",
            agent=self.ceo_agent,
            context=[research_task],
        )

        return [research_task, ceo_task]

    def run(self) -> str:
        result = self._crew.kickoff(
            inputs={"topic": self.context, "company": self.company}
        )
        return str(result)


class CFOReportCrew:

    def __init__(self, financial_context: str, company: str = "Company") -> None:
        self.financial_context = financial_context
        self.company = company
        self.cfo_agent = create_cfo_agent()
        self._crew = Crew(
            agents=[self.cfo_agent],
            tasks=self._build_tasks(),
            process=Process.sequential,
            verbose=True,
        )

    def _build_tasks(self) -> list:
        cfo_task = Task(
            description=(
                f"Analyze this financial context for {self.company}:\\n\\n"
                f"{self.financial_context}\\n\\n"
                "REQUIRED SECTIONS:\\n"
                "# CFO Report — Executive Financial Summary\\n"
                "## Revenue Snapshot\\n"
                "## Cost & Expense Breakdown\\n"
                "## Gross & Net Margin Analysis\\n"
                "## Burn Rate & Runway\\n"
                "## Unit Economics\\n"
                "## Top 3 Financial Risks\\n"
                "## Cost Optimization Opportunities\\n"
                "## 3 Scenarios (Best/Base/Worst)\\n"
                "## Recommended Financial Actions\\n\\n"
                "Use tables where possible. Be precise with numbers."
            ),
            expected_output="Professional CFO report with financial analysis",
            agent=self.cfo_agent,
        )

        return [cfo_task]

    def run(self) -> str:
        result = self._crew.kickoff(inputs={"topic": self.financial_context})
        return str(result)


class PromptEngineeringCrew:

    def __init__(self, original_prompt: str, use_case: str = "general") -> None:
        self.original_prompt = original_prompt
        self.use_case = use_case
        self.prompt_engineer = create_prompt_engineer()
        self._crew = Crew(
            agents=[self.prompt_engineer],
            tasks=self._build_tasks(),
            process=Process.sequential,
            verbose=True,
        )

    def _build_tasks(self) -> list:
        prompt_task = Task(
            description=(
                f"Analyze and improve this prompt:\\n\\n"
                f"ORIGINAL PROMPT:\\n{self.original_prompt}\\n\\n"
                f"USE CASE: {self.use_case}\\n\\n"
                "DELIVERABLES:\\n"
                "## Prompt Analysis\\n"
                "- Clarity score (1-10)\\n"
                "- Specificity score (1-10)\\n"
                "- Expected output quality (1-10)\\n\\n"
                "## Improved Prompt\\n"
                "(Full improved version)\\n\\n"
                "## Professional Prompt\\n"
                "(With system role, task, output contract)\\n\\n"
                "## Explanation\\n"
                "What changes were made and why"
            ),
            expected_output="Complete prompt engineering report",
            agent=self.prompt_engineer,
        )

        return [prompt_task]

    def run(self) -> str:
        result = self._crew.kickoff(inputs={"topic": self.use_case})
        return str(result)
'''


# ══════════════════════════════════════
#         CREATE ALL FILES
# ══════════════════════════════════════

created = 0
skipped = 0

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        print(f"⚠️  Exists: {path}")
        skipped += 1
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created: {path}")
        created += 1

print(f"\n{'='*50}")
print(f"✅ Created: {created} files")
print(f"⚠️  Skipped: {skipped} files")
print(f"{'='*50}")
print("Done! Now run: streamlit run app.py")