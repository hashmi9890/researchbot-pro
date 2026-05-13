"""
Configuration Manager
---------------------
Sab environment variables ek jagah manage hoti hain.
Puri application yahan se config read karti hai.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application-wide configuration (singleton pattern)"""

    # ── LLM ─────────────────────────────────────────
    GROQ_API_KEY : str   = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME   : str   = os.getenv("MODEL_NAME",   "groq/llama-3.3-70b-versatile")
    TEMPERATURE  : float = float(os.getenv("TEMPERATURE",  "0.3"))
    MAX_TOKENS   : int   = int(os.getenv("MAX_TOKENS",     "8192"))

    # ── Output ──────────────────────────────────────
    OUTPUT_DIR   : str   = os.getenv("OUTPUT_DIR",  "outputs")

    @classmethod
    def validate(cls) -> None:
        """
        App start hone se pehle config validate karo.
        Missing ya invalid config pe clear error dega.
        """
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "\n❌  GROQ_API_KEY is missing!\n"
                "    Steps to fix:\n"
                "    1. Go to https://console.groq.com  (free)\n"
                "    2. Create an API key\n"
                "    3. Add it to your .env file:\n"
                "       GROQ_API_KEY=your_key_here\n"
            )
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)


# Module-level singleton — import karke seedha use karo
config = Config()