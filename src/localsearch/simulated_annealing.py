from localsearch.local_search import LocalSearch
from model.state import State

class SimulatedAnnealing(LocalSearch):
    def __init__(self, initialState : State):
        super().__init__(initialState)

    def execute(self) -> list[State]:
        print("Executing Simulated Annealing on ...")
        for p in self.state.packages:
            print(p.id)
        return super().execute()