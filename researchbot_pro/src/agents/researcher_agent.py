"""
Researcher Agent
----------------
Web research karta hai using DuckDuckGo.
"""

from crewai import Agent
from src.config import config
from src.tools.search_tools import DuckDuckGoSearchTool


def create_researcher() -> Agent:
    return Agent(
        role="Senior Research Specialist",
        goal=(
            "Conduct thorough multi-angle web research on {topic}. "
            "Find recent credible data, statistics, expert opinions, "
            "key developments. Always cite source URLs."
        ),
        backstory=(
            "You are a veteran investigative journalist with 20 years of "
            "experience. You verify every claim from at least two sources "
            "and never fabricate information."
        ),
        tools            = [DuckDuckGoSearchTool()],
        llm              = config.MODEL_NAME,
        verbose          = True,
        allow_delegation = False,
        max_iter         = 3,
    )