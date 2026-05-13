"""
Writer Agent
------------
Professional Markdown report banata hai.
"""

from crewai import Agent
from src.config import config


def create_writer() -> Agent:
    return Agent(
        role="Professional Report Writer",
        goal=(
            "Transform research and analysis on {topic} into a polished "
            "800-1200 word professional Markdown report with all required "
            "sections and source citations."
        ),
        backstory=(
            "You are an award-winning technical writer published in Harvard "
            "Business Review. You transform dense research into compelling, "
            "well-structured narratives for all audiences."
        ),
        llm              = config.MODEL_NAME,
        verbose          = True,
        allow_delegation = False,
        max_iter         = 2,
    )