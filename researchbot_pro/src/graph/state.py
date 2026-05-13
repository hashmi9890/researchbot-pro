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
