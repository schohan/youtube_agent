from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel

class AgentResult(BaseModel):
    """
    Structure of the result of an agent execution.
    """
    success: bool
    data: Any
    error: str = ""


class BaseAgent(ABC):
    """
    Base class for all agents.
    """
    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> AgentResult:
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        pass