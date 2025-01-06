from pydantic import BaseModel
from typing import Any

class AgentResult(BaseModel):
    """
    Structure of the result of an agent execution.
    """
    success: bool = False
    data: Any
    error: str = ""
