"""
Executive Reports Crew
----------------------
CEO / CFO reports banata hai.
"""

from crewai import Crew, Task, Process
from src.agents.researcher_agent import create_researcher
from src.agents.ceo_agent import create_ceo_agent
from src.agents.cfo_agent import create_cfo_agent
from src.agents.prompt_agent import create_prompt_engineer


class CEOReportCrew:

    def __init__(self, context: str, company: str = "Company") -> None:
        self.context    = context
        self.company    = company
        self.researcher = create_researcher()
        self.ceo_agent  = create_ceo_agent()
        self._crew      = Crew(
            agents  = [self.researcher, self.ceo_agent],
            tasks   = self._build_tasks(),
            process = Process.sequential,
            verbose = True,
        )

    def _build_tasks(self) -> list:

        research_task = Task(
            description=(
                f"Research and gather data about: {self.context}\n"
                "Focus on: market position, competitors, opportunities, "
                "industry trends, and strategic landscape."
            ),
            expected_output="Comprehensive research on the topic with key insights",
            agent=self.researcher,
        )

        ceo_task = Task(
            description=(
                f"Write a CEO-level strategic report for {self.company}.\n\n"
                "REQUIRED SECTIONS:\n"
                "# Executive Summary (3 bullets max)\n"
                "## Situation Analysis\n"
                "## Top 3 Strategic Opportunities\n"
                "## Top 3 Critical Risks\n"
                "## Recommended Strategic Priorities\n"
                "## Decisions Required This Month\n"
                "## 30/60/90 Day Action Plan\n"
                "## KPI Dashboard (table format)\n"
                "## Bottom Line\n\n"
                "Write for a busy CEO. Be direct. No fluff."
            ),
            expected_output="Professional CEO report with all required sections",
            agent   = self.ceo_agent,
            context = [research_task],
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
        self.company           = company
        self.cfo_agent         = create_cfo_agent()
        self._crew             = Crew(
            agents  = [self.cfo_agent],
            tasks   = self._build_tasks(),
            process = Process.sequential,
            verbose = True,
        )

    def _build_tasks(self) -> list:

        cfo_task = Task(
            description=(
                f"Analyze this financial context for {self.company}:\n\n"
                f"{self.financial_context}\n\n"
                "REQUIRED SECTIONS:\n"
                "# CFO Report — Executive Financial Summary\n"
                "## Revenue Snapshot\n"
                "## Cost & Expense Breakdown\n"
                "## Gross & Net Margin Analysis\n"
                "## Burn Rate & Runway\n"
                "## Unit Economics\n"
                "## Cash Flow Position\n"
                "## Top 3 Financial Risks\n"
                "## Cost Optimization Opportunities\n"
                "## 3 Financial Scenarios (Best/Base/Worst)\n"
                "## Recommended Financial Actions\n\n"
                "Use tables where possible. Be precise with numbers."
            ),
            expected_output="Professional CFO report with financial analysis",
            agent=self.cfo_agent,
        )

        return [cfo_task]

    def run(self) -> str:
        result = self._crew.kickoff(
            inputs={"topic": self.financial_context}
        )
        return str(result)


class PromptEngineeringCrew:

    def __init__(self, original_prompt: str, use_case: str = "general") -> None:
        self.original_prompt = original_prompt
        self.use_case        = use_case
        self.prompt_engineer = create_prompt_engineer()
        self._crew           = Crew(
            agents  = [self.prompt_engineer],
            tasks   = self._build_tasks(),
            process = Process.sequential,
            verbose = True,
        )

    def _build_tasks(self) -> list:

        prompt_task = Task(
            description=(
                f"Analyze and improve this prompt:\n\n"
                f"ORIGINAL PROMPT:\n{self.original_prompt}\n\n"
                f"USE CASE: {self.use_case}\n\n"
                "DELIVERABLES:\n"
                "## Prompt Analysis\n"
                "- What works\n"
                "- What is missing\n"
                "- Clarity score (1-10)\n"
                "- Specificity score (1-10)\n"
                "- Expected output quality (1-10)\n\n"
                "## Improved Prompt\n"
                "(Full improved version)\n\n"
                "## Professional Prompt\n"
                "(With system role, task, output contract)\n\n"
                "## Few-Shot Example Version\n"
                "(With examples added)\n\n"
                "## Explanation\n"
                "What changes were made and why"
            ),
            expected_output=(
                "Complete prompt engineering report with:\n"
                "- Analysis scores\n"
                "- Improved prompt\n"
                "- Professional prompt\n"
                "- Few-shot version\n"
                "- Explanation"
            ),
            agent=self.prompt_engineer,
        )

        return [prompt_task]

    def run(self) -> str:
        result = self._crew.kickoff(
            inputs={"topic": self.use_case}
        )
        return str(result)