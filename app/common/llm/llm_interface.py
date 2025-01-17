from abc import ABC, abstractmethod
from typing import Any

class LLM(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def invoke(self, input) -> Any:
        pass

    @abstractmethod
    def stream(self, input) -> str:
        pass

    @abstractmethod
    def chat(self, input) -> str:
        pass


