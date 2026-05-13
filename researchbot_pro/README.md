# 🤖 ResearchBot Pro

> **AI-powered research agent** built with LangGraph + CrewAI + Groq LLM.
> Enter any topic → Get a professional research report automatically.

---

## ✨ Features
- 🔍 **Automatic web research** via DuckDuckGo (no API key needed)
- 🤖 **3-agent pipeline** — Researcher → Analyst → Writer
- 🔄 **LangGraph workflow** with validation, error handling & retry
- 💾 **Auto-saves** reports as Markdown files
- 🆓 **100% free** — Groq free tier + DuckDuckGo

## 🚀 Quick Start

```bash
cd researchbot_pro
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## 🏗️ Architecture
```
User Input
    ↓
[LangGraph Workflow]
    ├── Node 1: validate_input
    ├── Node 2: run_research  ← [CrewAI Crew]
    │       ├── Researcher Agent (DuckDuckGo)
    │       ├── Analyst Agent
    │       └── Writer Agent
    └── Node 3: save_report → outputs/
```

---
*Generated on May 13, 2026 by ResearchBot Pro Setup*
