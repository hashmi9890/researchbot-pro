"""
File Handler
------------
Research reports ko disk pe save karta hai.
"""

import os
import re
from datetime import datetime
from src.config import config


class FileHandler:

    def __init__(self) -> None:
        self._output_dir = config.OUTPUT_DIR
        os.makedirs(self._output_dir, exist_ok=True)

    @staticmethod
    def _sanitize(text: str, max_len: int = 50) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "",  text)
        text = re.sub(r"\s+",       "_", text).strip("_")
        return text[:max_len]

    @staticmethod
    def _header(topic: str) -> str:
        now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        return (
            f"# Research Report\n"
            f"**Topic:** {topic}  \n"
            f"**Generated:** {now}  \n"
            f"**Tool:** ResearchBot Pro — LangGraph + CrewAI + Groq\n\n"
            f"---\n\n"
        )

    def save(self, topic: str, content: str) -> str:
        timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = self._sanitize(topic)
        filename   = f"report_{clean_name}_{timestamp}.md"
        file_path  = os.path.join(self._output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(self._header(topic) + content)

        return os.path.abspath(file_path)
