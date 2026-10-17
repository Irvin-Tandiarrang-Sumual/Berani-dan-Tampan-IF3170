from abc import ABC, abstractmethod
from model.state import Problem
from dto import LocalSearchResult

class LocalSearch(ABC):
    def __init__(self, problem : Problem):
        super().__init__()
        self.problem = problem
        
    @abstractmethod
    def execute(self) -> LocalSearchResult:
        pass
