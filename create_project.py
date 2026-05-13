"""
╔══════════════════════════════════════════════════════════╗
║           ResearchBot Pro — Master Project Generator      ║
║        Ek command se poora project setup ho jayega        ║
║              LangGraph + CrewAI + Groq LLM                ║
╚══════════════════════════════════════════════════════════╝

Usage:
    python create_project.py
    python create_project.py --name my_research_bot
    python create_project.py --path /home/user/projects
"""

import os
import sys
import stat
import shutil
import argparse
import textwrap
import subprocess
from pathlib import Path
from datetime import datetime


# ═══════════════════════════════════════════════════
#                  CONSOLE COLORS
# ═══════════════════════════════════════════════════

class Color:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"

def log(symbol: str, message: str, color: str = Color.WHITE) -> None:
    print(f"{color}{symbol}  {message}{Color.RESET}")

def log_header(title: str) -> None:
    width = 60
    print(f"\n{Color.CYAN}{'═' * width}")
    print(f"  {title}")
    print(f"{'═' * width}{Color.RESET}\n")

def log_success(msg: str) -> None: log("✅", msg, Color.GREEN)
def log_info(msg: str)    -> None: log("ℹ️ ", msg, Color.CYAN)
def log_warn(msg: str)    -> None: log("⚠️ ", msg, Color.YELLOW)
def log_error(msg: str)   -> None: log("❌", msg, Color.RED)
def log_file(msg: str)    -> None: log("📄", msg, Color.DIM)


# ═══════════════════════════════════════════════════
#              FILE CONTENTS DICTIONARY
# ═══════════════════════════════════════════════════

def get_file_contents(project_name: str) -> dict:

    files = {}

    # ──────────────────────────────────────────
    #  ROOT FILES
    # ──────────────────────────────────────────

    files[".env.example"] = textwrap.dedent("""\
        # ─────────────────────────────────────────────
        # ResearchBot Pro — Environment Configuration
        # ─────────────────────────────────────────────
        # 1. Copy this file → rename to .env
        # 2. Fill in your actual values
        # 3. NEVER commit .env to git!
        #
        # Free Groq API Key: https://console.groq.com
        # ─────────────────────────────────────────────

        # ── LLM Configuration ──────────────────────
        GROQ_API_KEY=your_groq_api_key_here
        MODEL_NAME=groq/llama-3.3-70b-versatile
        TEMPERATURE=0.3
        MAX_TOKENS=8192

        # ── Output Configuration ────────────────────
        OUTPUT_DIR=outputs
        LOG_LEVEL=INFO
    """)

    files[".gitignore"] = textwrap.dedent("""\
        # ── Python ──────────────────────────────────
        __pycache__/
        *.py[cod]
        *$py.class
        *.pyo
        .Python
        build/
        dist/
        *.egg-info/
        .eggs/

        # ── Virtual Environment ──────────────────────
        venv/
        .venv/
        env/
        ENV/

        # ── Environment Variables ────────────────────
        .env
        *.env

        # ── Project Outputs ──────────────────────────
        outputs/*.md
        outputs/*.txt
        outputs/*.pdf
        !outputs/.gitkeep

        # ── IDE / Editor ────────────────────────────
        .vscode/settings.json
        .idea/
        *.swp
        *.swo
        .DS_Store
        Thumbs.db

        # ── Logs ─────────────────────────────────────
        logs/
        *.log
    """)

    files["requirements.txt"] = textwrap.dedent("""\
        # ─────────────────────────────────────────────
        # ResearchBot Pro — Python Dependencies
        # Install: pip install -r requirements.txt
        # Python : 3.10+
        # ─────────────────────────────────────────────

        # ── Core AI Frameworks ───────────────────────
        crewai==0.80.0
        crewai-tools==0.17.0
        langgraph==0.2.56
        langchain==0.3.13
        langchain-groq==0.2.3
        langchain-community==0.3.13

        # ── Free Web Search (No API Key) ─────────────
        duckduckgo-search==6.3.7

        # ── Utilities ────────────────────────────────
        python-dotenv==1.0.1
        pydantic==2.10.4
        rich==13.9.4
    """)

    files["README.md"] = textwrap.dedent(f"""\
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
        cd {project_name}
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
        *Generated on {datetime.now().strftime('%B %d, %Y')} by ResearchBot Pro Setup*
    """)

    # ──────────────────────────────────────────
    #  MAIN.PY
    # ──────────────────────────────────────────

    files["main.py"] = textwrap.dedent('''\
        """
        ╔══════════════════════════════════════════════╗
        ║         ResearchBot Pro — Entry Point         ║
        ║     LangGraph + CrewAI + Groq LLM Agent       ║
        ╚══════════════════════════════════════════════╝
        Usage:
            python main.py
        """

        import sys
        from rich.console import Console
        from rich.panel   import Panel
        from rich.prompt  import Prompt

        from src.config         import config
        from src.graph.workflow import ResearchWorkflow

        console = Console()


        def print_banner() -> None:
            console.print(
                Panel.fit(
                    "[bold cyan]🤖 ResearchBot Pro[/bold cyan]\\n"
                    "[dim]Powered by LangGraph + CrewAI + Groq LLM[/dim]\\n"
                    "[dim]Type a topic → Get a professional research report[/dim]",
                    border_style="cyan",
                    padding=(1, 4),
                )
            )


        def print_result(state: dict) -> None:
            console.print()
            if state.get("research_report"):
                console.print(
                    Panel(
                        f"✅ [bold green]Research Complete![/bold green]\\n\\n"
                        f"  📊 Words Generated  :  [bold]{state.get('word_count', 0)}[/bold]\\n"
                        f"  💾 Report Saved At  :  [bold]{state.get('output_file_path', 'N/A')}[/bold]",
                        border_style="green",
                        title="[bold]Results[/bold]",
                    )
                )
                report  = state["research_report"]
                preview = report[:600] + "\\n\\n[dim]... (open saved file for full report)[/dim]"
                console.print(
                    Panel(preview, title="📄 Report Preview", border_style="blue")
                )
            else:
                console.print(
                    Panel(
                        f"❌ [bold red]Research Failed[/bold red]\\n\\n"
                        f"  Error: {state.get('error_message', 'Unknown error')}",
                        border_style="red",
                    )
                )


        def main() -> None:
            print_banner()

            try:
                config.validate()
                console.print("✅ [green]Configuration loaded[/green]\\n")
            except ValueError as exc:
                console.print(f"[bold red]{exc}[/bold red]")
                sys.exit(1)

            workflow = ResearchWorkflow()

            while True:
                console.print("[bold]Commands:[/bold]")
                console.print("  • Enter a research topic to begin")
                console.print("  • Type [bold cyan]exit[/bold cyan] to quit\\n")

                topic = Prompt.ask("🔍 [bold]Research Topic[/bold]").strip()

                if topic.lower() in {"exit", "quit", "q"}:
                    console.print("\\n[bold cyan]Goodbye! 👋[/bold cyan]\\n")
                    break

                if not topic:
                    console.print("[yellow]⚠️  Please enter a topic.[/yellow]\\n")
                    continue

                final_state = workflow.run(topic=topic)
                print_result(final_state)

                again = Prompt.ask(
                    "\\n🔄 [bold]Research another topic?[/bold]",
                    choices=["yes", "no"],
                    default="yes",
                )
                if again == "no":
                    console.print("\\n[bold cyan]Goodbye! 👋[/bold cyan]\\n")
                    break


        if __name__ == "__main__":
            main()
    ''')

    # ──────────────────────────────────────────
    #  SRC PACKAGE
    # ──────────────────────────────────────────

    files["src/__init__.py"] = "# ResearchBot Pro — Source Package\n"

    files["src/config.py"] = textwrap.dedent('''\
        """
        Configuration Manager
        ---------------------
        Sab environment variables ek jagah manage hoti hain.
        """

        import os
        from dotenv import load_dotenv

        load_dotenv()


        class Config:
            GROQ_API_KEY : str   = os.getenv("GROQ_API_KEY", "")
            MODEL_NAME   : str   = os.getenv("MODEL_NAME",   "groq/llama-3.3-70b-versatile")
            TEMPERATURE  : float = float(os.getenv("TEMPERATURE",  "0.3"))
            MAX_TOKENS   : int   = int(os.getenv("MAX_TOKENS",     "8192"))
            OUTPUT_DIR   : str   = os.getenv("OUTPUT_DIR",  "outputs")

            @classmethod
            def validate(cls) -> None:
                if not cls.GROQ_API_KEY:
                    raise ValueError(
                        "\\n❌  GROQ_API_KEY is missing!\\n"
                        "    1. Go to https://console.groq.com  (free)\\n"
                        "    2. Create an API key\\n"
                        "    3. Add to .env file:\\n"
                        "       GROQ_API_KEY=your_key_here\\n"
                    )
                os.makedirs(cls.OUTPUT_DIR, exist_ok=True)


        config = Config()
    ''')

    # ──────────────────────────────────────────
    #  TOOLS
    # ──────────────────────────────────────────

    files["src/tools/__init__.py"] = textwrap.dedent("""\
        from .search_tools import DuckDuckGoSearchTool
        __all__ = ["DuckDuckGoSearchTool"]
    """)

    files["src/tools/search_tools.py"] = textwrap.dedent('''\
        """
        Search Tools
        ------------
        DuckDuckGo web search — free, no API key required.
        """

        from typing    import Type
        from pydantic  import BaseModel, Field
        from crewai.tools import BaseTool
        from duckduckgo_search import DDGS


        class _SearchInput(BaseModel):
            query      : str = Field(description="Search query string")
            max_results: int = Field(default=5, description="Max results (1-10)")


        class DuckDuckGoSearchTool(BaseTool):
            name        : str = "Web Search Tool"
            description : str = (
                "Search the web for current information on any topic. "
                "Returns titles, summaries, and source URLs. "
                "Use specific, focused queries for best results."
            )
            args_schema : Type[BaseModel] = _SearchInput

            def _run(self, query: str, max_results: int = 5) -> str:
                try:
                    with DDGS() as ddgs:
                        raw = list(ddgs.text(query, max_results=max_results))

                    if not raw:
                        return f"No results found for: \\'{query}\\'. Try broader query."

                    out = []
                    for i, item in enumerate(raw, 1):
                        out.append(
                            f"[Result {i}]\\n"
                            f"Title  : {item.get('title',  'N/A')}\\n"
                            f"Summary: {item.get('body',   'N/A')}\\n"
                            f"Source : {item.get('href',   'N/A')}\\n"
                        )
                    return "\\n".join(out)

                except Exception as exc:
                    return f"Search failed: {str(exc)}. Try a different query."
    ''')

    # ──────────────────────────────────────────
    #  AGENTS
    # ──────────────────────────────────────────

    files["src/agents/__init__.py"] = textwrap.dedent("""\
        from .researcher_agent import create_researcher
        from .analyst_agent    import create_analyst
        from .writer_agent     import create_writer
        __all__ = ["create_researcher", "create_analyst", "create_writer"]
    """)

    files["src/agents/researcher_agent.py"] = textwrap.dedent('''\
        """
        Researcher Agent
        ----------------
        Web research karta hai using DuckDuckGo.
        """

        from crewai        import Agent
        from langchain_groq import ChatGroq
        from src.config    import config
        from src.tools.search_tools import DuckDuckGoSearchTool


        def create_researcher() -> Agent:
            llm = ChatGroq(
                model      = config.MODEL_NAME,
                api_key    = config.GROQ_API_KEY,
                temperature= config.TEMPERATURE,
                max_tokens = config.MAX_TOKENS,
            )
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
                llm              = llm,
                verbose          = True,
                allow_delegation = False,
                max_iter         = 3,
            )
    ''')

    files["src/agents/analyst_agent.py"] = textwrap.dedent('''\
        """
        Analyst Agent
        -------------
        Raw research ko structured insights mein convert karta hai.
        """

        from crewai        import Agent
        from langchain_groq import ChatGroq
        from src.config    import config


        def create_analyst() -> Agent:
            llm = ChatGroq(
                model      = config.MODEL_NAME,
                api_key    = config.GROQ_API_KEY,
                temperature= config.TEMPERATURE,
                max_tokens = config.MAX_TOKENS,
            )
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
                llm              = llm,
                verbose          = True,
                allow_delegation = False,
                max_iter         = 2,
            )
    ''')

    files["src/agents/writer_agent.py"] = textwrap.dedent('''\
        """
        Writer Agent
        ------------
        Professional Markdown report banata hai.
        """

        from crewai        import Agent
        from langchain_groq import ChatGroq
        from src.config    import config


        def create_writer() -> Agent:
            llm = ChatGroq(
                model      = config.MODEL_NAME,
                api_key    = config.GROQ_API_KEY,
                temperature= 0.4,
                max_tokens = config.MAX_TOKENS,
            )
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
                llm              = llm,
                verbose          = True,
                allow_delegation = False,
                max_iter         = 2,
            )
    ''')

    # ──────────────────────────────────────────
    #  CREW
    # ──────────────────────────────────────────

    files["src/crew/__init__.py"] = textwrap.dedent("""\
        from .research_crew import ResearchCrew
        __all__ = ["ResearchCrew"]
    """)

    files["src/crew/research_crew.py"] = textwrap.dedent('''\
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
                        f"Research the topic: \\"{self.topic}\\"\\n\\n"
                        "DELIVERABLES:\\n"
                        "1. Current state — what is happening right now?\\n"
                        "2. Recent developments — last 6 months\\n"
                        "3. Key statistics and data points\\n"
                        "4. Major players / companies / experts\\n"
                        "5. Challenges and open problems\\n"
                        "6. Future outlook / predictions\\n\\n"
                        "Search at least 3 distinct angles. "
                        "Cite every finding with source URL."
                    ),
                    expected_output=(
                        "Structured research report with:\\n"
                        "- 5+ verified key findings with source URLs\\n"
                        "- Important statistics\\n"
                        "- Recent news and developments\\n"
                        "- Full source list"
                    ),
                    agent=self.researcher,
                )

                analysis_task = Task(
                    description=(
                        f"Analyze all research findings about \\"{self.topic}\\"\\n\\n"
                        "DELIVERABLES:\\n"
                        "1. Top 5 key insights (numbered, specific)\\n"
                        "2. Trend analysis\\n"
                        "3. SWOT analysis\\n"
                        "4. Impact assessment\\n"
                        "5. Top 3 actionable recommendations\\n\\n"
                        "Be objective and data-driven. Use numbers where possible."
                    ),
                    expected_output=(
                        "Structured analysis with:\\n"
                        "- 5 numbered key insights\\n"
                        "- Trend analysis paragraph\\n"
                        "- SWOT table\\n"
                        "- 3 specific recommendations"
                    ),
                    agent   = self.analyst,
                    context = [research_task],
                )

                writing_task = Task(
                    description=(
                        f"Write a professional report on \\"{self.topic}\\"\\n\\n"
                        "REQUIRED STRUCTURE:\\n"
                        "# [Compelling Title]\\n"
                        "## Executive Summary\\n"
                        "## Key Findings\\n"
                        "## Detailed Analysis\\n"
                        "## Trends & Future Outlook\\n"
                        "## Recommendations\\n"
                        "## Sources\\n\\n"
                        "Format: Markdown. Length: 800-1200 words."
                    ),
                    expected_output=(
                        "Complete professional Markdown report:\\n"
                        "- All 6 sections present\\n"
                        "- 800-1200 words\\n"
                        "- Proper Markdown formatting\\n"
                        "- Sources section with all URLs"
                    ),
                    agent   = self.writer,
                    context = [research_task, analysis_task],
                )

                return [research_task, analysis_task, writing_task]

            def run(self) -> str:
                result = self._crew.kickoff(inputs={"topic": self.topic})
                return str(result)
    ''')

    # ──────────────────────────────────────────
    #  GRAPH (LANGGRAPH)
    # ──────────────────────────────────────────

    files["src/graph/__init__.py"] = textwrap.dedent("""\
        from .state    import ResearchState, WorkflowStatus
        from .workflow import ResearchWorkflow
        __all__ = ["ResearchState", "WorkflowStatus", "ResearchWorkflow"]
    """)

    files["src/graph/state.py"] = textwrap.dedent('''\
        """
        LangGraph State Schema
        ----------------------
        Workflow ka shared memory.
        Har node yeh state read aur write karta hai.
        """

        from typing            import Optional
        from typing_extensions import TypedDict
        from enum              import Enum


        class WorkflowStatus(str, Enum):
            PENDING     = "pending"
            VALIDATING  = "validating"
            RESEARCHING = "researching"
            COMPLETED   = "completed"
            FAILED      = "failed"


        class ResearchState(TypedDict):
            topic              : str
            status             : WorkflowStatus
            current_step       : str
            error_message      : Optional[str]
            is_valid           : bool
            validation_message : str
            research_report    : Optional[str]
            output_file_path   : Optional[str]
            word_count         : int
    ''')

    files["src/graph/workflow.py"] = textwrap.dedent('''\
        """
        LangGraph Workflow
        ------------------
        Research process ka state machine.

        Flow:
            START → validate_input
                ├── (invalid) → handle_error → END
                └── (valid)   → run_research
                        ├── (failed)  → handle_error → END
                        └── (success) → save_report  → END
        """

        from langgraph.graph import StateGraph, START, END
        from rich.console    import Console
        from rich.panel      import Panel

        from src.graph.state        import ResearchState, WorkflowStatus
        from src.crew.research_crew import ResearchCrew
        from src.utils.file_handler import FileHandler

        console = Console()


        class ResearchWorkflow:

            def __init__(self) -> None:
                self._file_handler = FileHandler()
                self._graph        = self._build_graph()

            # ═══════════════ NODES ═══════════════

            def validate_input(self, state: ResearchState) -> ResearchState:
                console.print(
                    Panel("🔍 [bold cyan]Step 1 / 3 — Validating Input[/bold cyan]",
                          border_style="cyan")
                )
                topic = state["topic"].strip()

                if not topic:
                    return {**state,
                            "status": WorkflowStatus.FAILED,
                            "is_valid": False,
                            "validation_message": "Topic cannot be empty.",
                            "error_message": "Empty topic"}

                if len(topic) < 3:
                    return {**state,
                            "status": WorkflowStatus.FAILED,
                            "is_valid": False,
                            "validation_message": f"Topic too short: \\'{topic}\\'. Min 3 chars.",
                            "error_message": "Topic too short"}

                if len(topic) > 200:
                    return {**state,
                            "status": WorkflowStatus.FAILED,
                            "is_valid": False,
                            "validation_message": "Topic too long. Max 200 characters.",
                            "error_message": "Topic too long"}

                console.print(f"  ✅ Valid: [bold green]\\'{topic}\\'[/bold green]")
                return {**state,
                        "topic"             : topic,
                        "status"            : WorkflowStatus.RESEARCHING,
                        "current_step"      : "research",
                        "is_valid"          : True,
                        "validation_message": "Input is valid."}

            def run_research(self, state: ResearchState) -> ResearchState:
                topic = state["topic"]
                console.print(
                    Panel(
                        f"🤖 [bold yellow]Step 2 / 3 — Running Research Crew[/bold yellow]\\n"
                        f"  Topic  : [bold]{topic}[/bold]\\n"
                        f"  Agents : Researcher → Analyst → Writer",
                        border_style="yellow",
                    )
                )
                try:
                    crew   = ResearchCrew(topic=topic)
                    report = crew.run()
                    words  = len(report.split())
                    console.print(f"\\n  ✅ Done — [bold green]{words:,} words[/bold green]")
                    return {**state,
                            "status"         : WorkflowStatus.COMPLETED,
                            "current_step"   : "save",
                            "research_report": report,
                            "word_count"     : words,
                            "error_message"  : None}
                except Exception as exc:
                    console.print(f"\\n  ❌ Failed: [red]{exc}[/red]")
                    return {**state,
                            "status"         : WorkflowStatus.FAILED,
                            "current_step"   : "error",
                            "error_message"  : str(exc),
                            "research_report": None,
                            "word_count"     : 0}

            def save_report(self, state: ResearchState) -> ResearchState:
                console.print(
                    Panel("💾 [bold green]Step 3 / 3 — Saving Report[/bold green]",
                          border_style="green")
                )
                try:
                    path = self._file_handler.save(
                        topic  = state["topic"],
                        content= state["research_report"],
                    )
                    console.print(f"  ✅ Saved: [bold]{path}[/bold]")
                    return {**state, "output_file_path": path, "current_step": "done"}
                except Exception as exc:
                    console.print(f"  ⚠️  Save failed: [yellow]{exc}[/yellow]")
                    return {**state,
                            "output_file_path": None,
                            "error_message"   : f"Save failed: {exc}"}

            def handle_error(self, state: ResearchState) -> ResearchState:
                console.print(
                    Panel(
                        f"❌ [bold red]Workflow Error[/bold red]\\n\\n"
                        f"  Step  : {state.get('current_step', 'unknown')}\\n"
                        f"  Reason: {state.get('error_message', 'Unknown error')}",
                        border_style="red",
                    )
                )
                return {**state, "current_step": "failed"}

            # ═══════════════ ROUTING ═══════════════

            def _route_after_validation(self, state: ResearchState) -> str:
                return "run_research" if state["is_valid"] else "handle_error"

            def _route_after_research(self, state: ResearchState) -> str:
                return "save_report" if state["status"] == WorkflowStatus.COMPLETED else "handle_error"

            # ═══════════════ GRAPH ═════════════════

            def _build_graph(self):
                graph = StateGraph(ResearchState)

                graph.add_node("validate_input", self.validate_input)
                graph.add_node("run_research",   self.run_research)
                graph.add_node("save_report",    self.save_report)
                graph.add_node("handle_error",   self.handle_error)

                graph.add_edge(START,         "validate_input")
                graph.add_edge("save_report",  END)
                graph.add_edge("handle_error", END)

                graph.add_conditional_edges(
                    "validate_input",
                    self._route_after_validation,
                    {"run_research": "run_research", "handle_error": "handle_error"},
                )
                graph.add_conditional_edges(
                    "run_research",
                    self._route_after_research,
                    {"save_report": "save_report", "handle_error": "handle_error"},
                )

                return graph.compile()

            def run(self, topic: str) -> dict:
                initial: ResearchState = {
                    "topic"             : topic,
                    "status"            : WorkflowStatus.PENDING,
                    "current_step"      : "validate",
                    "error_message"     : None,
                    "is_valid"          : False,
                    "validation_message": "",
                    "research_report"   : None,
                    "output_file_path"  : None,
                    "word_count"        : 0,
                }
                return self._graph.invoke(initial)
    ''')

    # ──────────────────────────────────────────
    #  UTILS
    # ──────────────────────────────────────────

    files["src/utils/__init__.py"] = textwrap.dedent("""\
        from .file_handler import FileHandler
        __all__ = ["FileHandler"]
    """)

    files["src/utils/file_handler.py"] = textwrap.dedent('''\
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
                    f"# Research Report\\n"
                    f"**Topic:** {topic}  \\n"
                    f"**Generated:** {now}  \\n"
                    f"**Tool:** ResearchBot Pro — LangGraph + CrewAI + Groq\\n\\n"
                    f"---\\n\\n"
                )

            def save(self, topic: str, content: str) -> str:
                timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
                clean_name = self._sanitize(topic)
                filename   = f"report_{clean_name}_{timestamp}.md"
                file_path  = os.path.join(self._output_dir, filename)

                with open(file_path, "w", encoding="utf-8") as fh:
                    fh.write(self._header(topic) + content)

                return os.path.abspath(file_path)
    ''')

    # ──────────────────────────────────────────
    #  PLACEHOLDER
    # ──────────────────────────────────────────

    files["outputs/.gitkeep"] = (
        "# Keeps outputs/ in git.\n"
        "# Actual reports are gitignored.\n"
    )

    return files


# ═══════════════════════════════════════════════════
#              PROJECT GENERATOR CORE
# ═══════════════════════════════════════════════════

class ProjectGenerator:

    DIRECTORIES = [
        "src",
        "src/agents",
        "src/crew",
        "src/graph",
        "src/tools",
        "src/utils",
        "outputs",
    ]

    def __init__(self, project_name: str, base_path: str = ".") -> None:
        self.project_name   = project_name
        self.root           = Path(base_path) / project_name
        self._created_dirs  : list = []
        self._created_files : list = []
        self._skipped_files : list = []
        self._failed        : list = []

    def _create_directories(self) -> None:
        log_header("Creating Directory Structure")
        self.root.mkdir(parents=True, exist_ok=True)
        log_success(f"Project root: {self.root}")
        for directory in self.DIRECTORIES:
            dir_path = self.root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self._created_dirs.append(dir_path)
            log_success(f"  📁 {directory}/")

    def _write_files(self) -> None:
        log_header("Writing Source Files")
        file_map = get_file_contents(self.project_name)
        for rel_path, content in file_map.items():
            file_path = self.root / rel_path
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                if file_path.exists():
                    self._skipped_files.append(file_path)
                    log_warn(f"  Skipped (exists): {rel_path}")
                    continue
                file_path.write_text(content, encoding="utf-8")
                self._created_files.append(file_path)
                log_file(f"  {rel_path}")
            except Exception as exc:
                self._failed.append((rel_path, str(exc)))
                log_error(f"  FAILED: {rel_path} — {exc}")

    def _copy_env(self) -> None:
        src_path = self.root / ".env.example"
        dst_path = self.root / ".env"
        if dst_path.exists():
            log_warn(".env already exists — skipped")
            return
        if src_path.exists():
            shutil.copy(src_path, dst_path)
            log_success(".env created from .env.example")
            log_info("  ⚡ Open .env → add your GROQ_API_KEY")

    def _print_summary(self) -> None:
        log_header("Setup Summary")
        print(f"{Color.GREEN}  ✅ Directories : {len(self._created_dirs)}{Color.RESET}")
        print(f"{Color.GREEN}  ✅ Files        : {len(self._created_files)}{Color.RESET}")
        if self._skipped_files:
            print(f"{Color.YELLOW}  ⚠️  Skipped      : {len(self._skipped_files)}{Color.RESET}")
        if self._failed:
            print(f"{Color.RED}  ❌ Failed       : {len(self._failed)}{Color.RESET}")
            for f, err in self._failed:
                print(f"{Color.RED}     {f}: {err}{Color.RESET}")

    def _print_next_steps(self) -> None:
        log_header("🚀 Next Steps")
        steps = [
            ("1", "Project mein jao",
             f"cd {self.project_name}"),
            ("2", "Dependencies install karo",
             "pip install -r requirements.txt"),
            ("3", "Groq API key daalo (FREE)",
             "# https://console.groq.com\n"
             f"       # .env → GROQ_API_KEY=your_key"),
            ("4", "Run karo!",
             "python main.py"),
        ]
        for num, title, cmd in steps:
            print(f"\n  {Color.CYAN}{Color.BOLD}Step {num}: {title}{Color.RESET}")
            print(f"  {Color.DIM}$ {cmd}{Color.RESET}")

        print(f"\n{Color.GREEN}{Color.BOLD}")
        print("  ════════════════════════════════════════")
        print("   Project Ready! Happy Researching 🎉")
        print("  ════════════════════════════════════════")
        print(Color.RESET)

    def generate(self) -> bool:
        print(f"\n{Color.CYAN}{Color.BOLD}")
        print("  ╔═══════════════════════════════════════╗")
        print("  ║   ResearchBot Pro — Project Generator  ║")
        print("  ╚═══════════════════════════════════════╝")
        print(Color.RESET)

        log_info(f"Project : {self.project_name}")
        log_info(f"Path    : {self.root.resolve()}")

        try:
            self._create_directories()
            self._write_files()
            self._copy_env()
            self._print_summary()
            self._print_next_steps()
            return True
        except KeyboardInterrupt:
            log_warn("\nInterrupted by user.")
            return False
        except Exception as exc:
            log_error(f"Critical failure: {exc}")
            return False


# ═══════════════════════════════════════════════════
#                    ENTRY POINT
# ═══════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ResearchBot Pro — Automatic Project Generator",
    )
    parser.add_argument("--name", "-n", default="researchbot_pro",
                        help="Project folder name (default: researchbot_pro)")
    parser.add_argument("--path", "-p", default=".",
                        help="Parent directory (default: current directory)")
    return parser.parse_args()


if __name__ == "__main__":
    args      = parse_args()
    generator = ProjectGenerator(
        project_name = args.name,
        base_path    = args.path,
    )
    success = generator.generate()
    sys.exit(0 if success else 1) 
