"""
Prompt Engineering Agent
------------------------
Prompts analyze, improve aur optimize karta hai.
"""

from crewai import Agent
from src.config import config


def create_prompt_engineer() -> Agent:
    return Agent(
        role="Senior Prompt Engineer & LLM Optimization Specialist",
        goal=(
            "Analyze, improve, and optimize prompts for maximum "
            "LLM performance. Apply best practices: clear instructions, "
            "role assignment, output contracts, few-shot examples, "
            "chain-of-thought, and structured formatting."
        ),
        backstory=(
            "You are one of the world's leading prompt engineers, "
            "having worked with GPT-4, Claude, Llama, and Gemini. "
            "You understand token efficiency, context windows, "
            "hallucination prevention, and output consistency. "
            "You transform vague prompts into precision instruments."
        ),
        llm              = config.MODEL_NAME,
        verbose          = True,
        allow_delegation = False,
        max_iter         = 2,
    )