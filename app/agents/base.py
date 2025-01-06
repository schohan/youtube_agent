from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel

class BaseAgent(ABC):
    """
    Base class for all agents.
    """
    @abstractmethod
    async def execute(self, input: str) -> Any:
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        pass