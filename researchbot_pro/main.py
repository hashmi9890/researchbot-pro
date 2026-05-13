"""
ResearchBot Pro — Entry Point
LangGraph + CrewAI + Groq LLM Agent
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
            "[bold cyan]🤖 ResearchBot Pro[/bold cyan]\n"
            "[dim]Powered by LangGraph + CrewAI + Groq LLM[/dim]\n"
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
                f"✅ [bold green]Research Complete![/bold green]\n\n"
                f"  📊 Words Generated  :  [bold]{state.get('word_count', 0)}[/bold]\n"
                f"  💾 Report Saved At  :  [bold]{state.get('output_file_path', 'N/A')}[/bold]",
                border_style="green",
                title="[bold]Results[/bold]",
            )
        )
        report  = state["research_report"]
        preview = report[:600] + "\n\n[dim]... (open saved file for full report)[/dim]"
        console.print(
            Panel(preview, title="📄 Report Preview", border_style="blue")
        )
    else:
        console.print(
            Panel(
                f"❌ [bold red]Research Failed[/bold red]\n\n"
                f"  Error: {state.get('error_message', 'Unknown error')}",
                border_style="red",
            )
        )


def main() -> None:
    print_banner()

    try:
        config.validate()
        console.print("✅ [green]Configuration loaded[/green]\n")
    except ValueError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        sys.exit(1)

    workflow = ResearchWorkflow()

    while True:
        console.print("[bold]Commands:[/bold]")
        console.print("  • Enter a research topic to begin")
        console.print("  • Type [bold cyan]exit[/bold cyan] to quit\n")

        topic = Prompt.ask("🔍 [bold]Research Topic[/bold]").strip()

        if topic.lower() in {"exit", "quit", "q"}:
            console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
            break

        if not topic:
            console.print("[yellow]⚠️  Please enter a topic.[/yellow]\n")
            continue

        final_state = workflow.run(topic=topic)
        print_result(final_state)

        again = Prompt.ask(
            "\n🔄 [bold]Research another topic?[/bold]",
            choices=["yes", "no"],
            default="yes",
        )
        if again == "no":
            console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
            break


if __name__ == "__main__":
    main()