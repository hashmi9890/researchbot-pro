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
                return f"No results found for: \'{query}\'. Try broader query."

            out = []
            for i, item in enumerate(raw, 1):
                out.append(
                    f"[Result {i}]\n"
                    f"Title  : {item.get('title',  'N/A')}\n"
                    f"Summary: {item.get('body',   'N/A')}\n"
                    f"Source : {item.get('href',   'N/A')}\n"
                )
            return "\n".join(out)

        except Exception as exc:
            return f"Search failed: {str(exc)}. Try a different query."
