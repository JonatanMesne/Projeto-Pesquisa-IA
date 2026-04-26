from abc import ABC
from world_objects.world_object import WorldObject

class Entity(ABC):
    id = 0
    #construtor
    def __init__(self, appearence, health, vision_range):
        self.appearence = appearence
        self.health = health
        self.vision_range = vision_range
        self.vision_data = []
        self.id_vision_data = []
        self.standing_on: WorldObject #tile type where the agent is currently located (i.e. ground, item, etc)
        self.position = [-1, -1] #agent's position in the world grid
        self.is_solid = True
        # self.vector = [self.health, self.id_vision_data, self.position, self.standing_on.id]
        
    def print_vision_data(self):
        print("\nVision Data:")
        if len(self.vision_data) == 0:
            print("No vision data available.")
        else:
            for row in self.vision_data:
                print(' '.join(obj.appearence if obj is not None else 'None' for obj in row))
                
    def find_open_space(self, world_grid, position) -> list[int]:
        sum_for_x = 1
        sum_for_y = 1
        while True:
            if(world_grid[position[0]][position[1]].is_solid):
                if(position[0] == len(world_grid) - 1):
                    sum_for_x = -1
                elif(position[0] == 0):
                    sum_for_x = 1
                position[0] += sum_for_x
            else:
                break
            if(world_grid[position[0]][position[1]].is_solid):
                if(position[1] == len(world_grid[0]) - 1):
                    sum_for_y = -1
                elif(position[1] == 0):
                    sum_for_y = 1
                position[1] += sum_for_y
            else:
                break
        return position
    
    def place_entity(self, world_grid, position):
        if world_grid[position[0]][position[1]].is_solid:
            position = self.find_open_space(world_grid, position)
        self.standing_on = world_grid[position[0]][position[1]]
        world_grid[position[0]][position[1]] = self
        self.position = position
        
    def __str__(self) -> str:
        return self.appearence
        