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
                    "validation_message": f"Topic too short: \'{topic}\'. Min 3 chars.",
                    "error_message": "Topic too short"}

        if len(topic) > 200:
            return {**state,
                    "status": WorkflowStatus.FAILED,
                    "is_valid": False,
                    "validation_message": "Topic too long. Max 200 characters.",
                    "error_message": "Topic too long"}

        console.print(f"  ✅ Valid: [bold green]\'{topic}\'[/bold green]")
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
                f"🤖 [bold yellow]Step 2 / 3 — Running Research Crew[/bold yellow]\n"
                f"  Topic  : [bold]{topic}[/bold]\n"
                f"  Agents : Researcher → Analyst → Writer",
                border_style="yellow",
            )
        )
        try:
            crew   = ResearchCrew(topic=topic)
            report = crew.run()
            words  = len(report.split())
            console.print(f"\n  ✅ Done — [bold green]{words:,} words[/bold green]")
            return {**state,
                    "status"         : WorkflowStatus.COMPLETED,
                    "current_step"   : "save",
                    "research_report": report,
                    "word_count"     : words,
                    "error_message"  : None}
        except Exception as exc:
            console.print(f"\n  ❌ Failed: [red]{exc}[/red]")
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
                f"❌ [bold red]Workflow Error[/bold red]\n\n"
                f"  Step  : {state.get('current_step', 'unknown')}\n"
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
