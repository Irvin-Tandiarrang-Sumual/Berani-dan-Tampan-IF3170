from abc import ABC, abstractmethod
from model.state import State

class LocalSearch(ABC):
    def __init__(self, initialState : State):
        super().__init__()
        self.state = initialState
        
    @abstractmethod
    def execute(self) -> list[State]:
        pass
