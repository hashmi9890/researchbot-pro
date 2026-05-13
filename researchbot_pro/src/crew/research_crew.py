"""
Research Crew
-------------
3-agent CrewAI pipeline:
    Researcher → Analyst → Writer
"""

from crewai  import Crew, Task, Process
from src.agents import create_researcher, create_analyst, create_writer


class ResearchCrew:

    def __init__(self, topic: str) -> None:
        self.topic      = topic
        self.researcher = create_researcher()
        self.analyst    = create_analyst()
        self.writer     = create_writer()
        self._tasks     = self._build_tasks()
        self._crew      = Crew(
            agents  = [self.researcher, self.analyst, self.writer],
            tasks   = self._tasks,
            process = Process.sequential,
            verbose = True,
        )

    def _build_tasks(self) -> list:

        research_task = Task(
            description=(
                f"Research the topic: \"{self.topic}\"\n\n"
                "DELIVERABLES:\n"
                "1. Current state — what is happening right now?\n"
                "2. Recent developments — last 6 months\n"
                "3. Key statistics and data points\n"
                "4. Major players / companies / experts\n"
                "5. Challenges and open problems\n"
                "6. Future outlook / predictions\n\n"
                "Search at least 3 distinct angles. "
                "Cite every finding with source URL."
            ),
            expected_output=(
                "Structured research report with:\n"
                "- 5+ verified key findings with source URLs\n"
                "- Important statistics\n"
                "- Recent news and developments\n"
                "- Full source list"
            ),
            agent=self.researcher,
        )

        analysis_task = Task(
            description=(
                f"Analyze all research findings about \"{self.topic}\"\n\n"
                "DELIVERABLES:\n"
                "1. Top 5 key insights (numbered, specific)\n"
                "2. Trend analysis\n"
                "3. SWOT analysis\n"
                "4. Impact assessment\n"
                "5. Top 3 actionable recommendations\n\n"
                "Be objective and data-driven. Use numbers where possible."
            ),
            expected_output=(
                "Structured analysis with:\n"
                "- 5 numbered key insights\n"
                "- Trend analysis paragraph\n"
                "- SWOT table\n"
                "- 3 specific recommendations"
            ),
            agent   = self.analyst,
            context = [research_task],
        )

        writing_task = Task(
            description=(
                f"Write a professional report on \"{self.topic}\"\n\n"
                "REQUIRED STRUCTURE:\n"
                "# [Compelling Title]\n"
                "## Executive Summary\n"
                "## Key Findings\n"
                "## Detailed Analysis\n"
                "## Trends & Future Outlook\n"
                "## Recommendations\n"
                "## Sources\n\n"
                "Format: Markdown. Length: 800-1200 words."
            ),
            expected_output=(
                "Complete professional Markdown report:\n"
                "- All 6 sections present\n"
                "- 800-1200 words\n"
                "- Proper Markdown formatting\n"
                "- Sources section with all URLs"
            ),
            agent   = self.writer,
            context = [research_task, analysis_task],
        )

        return [research_task, analysis_task, writing_task]

    def run(self) -> str:
        result = self._crew.kickoff(inputs={"topic": self.topic})
        return str(result)
