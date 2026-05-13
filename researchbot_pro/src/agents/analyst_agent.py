"""
Analyst Agent
-------------
Raw research ko structured insights mein convert karta hai.
"""

from crewai import Agent
from src.config import config


def create_analyst() -> Agent:
    return Agent(
        role="Strategic Data Analyst",
        goal=(
            "Analyze research findings on {topic}. Extract key insights, "
            "identify patterns and trends, perform SWOT analysis, and "
            "produce data-backed actionable recommendations."
        ),
        backstory=(
            "You are a McKinsey-trained senior analyst. Every claim is "
            "backed by specific data. You identify what others miss and "
            "never make vague statements."
        ),
        llm              = config.MODEL_NAME,
        verbose          = True,
        allow_delegation = False,
        max_iter         = 2,
    )