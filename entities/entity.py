from abc import ABC
from world_objects.world_object import WorldObject

class Entity(ABC):
    #construtor
    def __init__(self, appearence, health, vision_range):
        self.appearence = appearence
        self.health = health
        self.vision_range = vision_range
        self.vision_data = []
        self.possible_actions = None
        self.standing_on: WorldObject #tile type where the agent is currently located (i.e. ground, item, etc)
        self.position = [-1, -1] #agent's position in the world grid
        self.is_solid = True
        
    def print_vision_data(self):
        print("Vision Data:")
        if len(self.vision_data) == 0:
            print("No vision data available.")
        else:
            for row in self.vision_data:
                print(' '.join(obj.appearence if obj is not None else 'None' for obj in row))
                
    def place_entity(self, world_grid, position):
        self.standing_on = world_grid[position[0]][position[1]]
        world_grid[position[0]][position[1]] = self
        self.position = position
        
    def __str__(self) -> str:
        return self.appearence
        