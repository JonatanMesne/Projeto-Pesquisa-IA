from abc import ABC, abstractmethod

class Action(ABC):
    def __init__(self, duration = 1):
        super().__init__()
        self.duration = duration
        
    @staticmethod
    @abstractmethod
    def action(state) -> bool: #passes the state and agent as parameters   | returns True if action was successful, False otherwise
        pass
    
    def advance_time(self, state):
        state.time_elapsed += self.duration