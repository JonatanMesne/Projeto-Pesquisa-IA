from abc import abstractmethod

class Action():
    duration = 0
    need_direction = False
    need_index = False
    id = 999
        
    @staticmethod
    @abstractmethod
    def action(state) -> bool: #passes the state and agent as parameters   | returns True if action was successful, False otherwise
        pass