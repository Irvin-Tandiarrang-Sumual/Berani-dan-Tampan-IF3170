from abc import ABC, abstractmethod
from model.problem import Problem
from localsearch.dto import LocalSearchResult

class LocalSearch(ABC):
    def __init__(self, problem : Problem):
        super().__init__()
        self.problem = problem
        
    @abstractmethod
    def execute(self) -> LocalSearchResult:
        pass
