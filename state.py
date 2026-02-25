from entities.agent import Agent
from entities.zombie import Zombie

class State:
    def __init__(self):
        self.entity_direction = 0  # 1 (up) | 2 (right) | 3 (down) | 4 (left)
        self.agent: Agent
        self.zombie: Zombie | None = None  # Store the current zombie in the state for access in actions
        self.map_grid = []
        self.time_elapsed = 0
        self.index = -1
        
    def print_self(self):
        print("Agent Direction:", self.entity_direction)
        print("Map Grid:")
        for row in self.map_grid:
            print(' '.join(row.appearence for row in row))
            
    def get_world_object_in_front(self):
        WO_position = self.agent.position.copy()
        #direction = 1 (up) | 2 (right) | 3 (down) | 4 (left)
        if self.entity_direction == 1:
            WO_position[0] -= 1
        elif self.entity_direction == 2:
            WO_position[1] += 1
        elif self.entity_direction == 3:
            WO_position[0] += 1
        elif self.entity_direction == 4:
            WO_position[1] -= 1
        return self.map_grid[WO_position[0]][WO_position[1]]
    
    def advance_time(self):
        self.time_elapsed += 1
        
    def entity_death(self, entity):
        self.map_grid[entity.position[0]][entity.position[1]] = entity.standing_on
        # if entity == self.zombie:
        #     self.zombie = None