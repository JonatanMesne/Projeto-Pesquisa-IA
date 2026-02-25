from entities.entity import Entity
from actions.update_vision import UpdateVision
from actions.walk import Walk
from entities.agent import Agent
from world_objects.ground import Ground
import random

class Zombie(Entity):
    #construtor
    def __init__(self, appearence = 'Z', health = 20, vision_range = 2, damage = 5):
        super().__init__(appearence, health, vision_range)
        self.damage = damage
        
    def print_status(self):
        print(f'Health: {self.health}')
        
        
    def zombieAction(self, state):
        # Behavior logic for the zombie
        state.zombie = self  # Store the zombie in the state for access in actions
        UpdateVision.action(state)  # Update vision data
        state.entity_direction = 0  # Reset direction
        distance_to_agent = [0, 0]
        for i in range(len(self.vision_data)):
            for j in range(len(self.vision_data[i])):
                obj = self.vision_data[i][j]
                if obj is not None and isinstance(obj, Agent):
                    distance_to_agent[0] = obj.position[0] - self.position[0]
                    distance_to_agent[1] = obj.position[1] - self.position[1]
                    if abs(distance_to_agent[0]) >= abs(distance_to_agent[1]):
                        if distance_to_agent[0] < 0:
                            state.entity_direction = 1  # up
                        else:
                            state.entity_direction = 3  # down
                    else:
                        if distance_to_agent[1] < 0:
                            state.entity_direction = 4  # left
                        else:
                            state.entity_direction = 2  # right
                    break
        if state.entity_direction == 0:
            state.entity_direction = random.randint(1, 4)
        if abs(distance_to_agent[0]) + abs(distance_to_agent[1]) == 1:
            # Attack the agent
            state.agent.health -= self.damage
        else:
            zombie_direction = state.entity_direction
            if not Walk.action(state):
                if zombie_direction == 1 or zombie_direction == 3:
                    if distance_to_agent[1] < 0:
                        state.entity_direction = 4  # left
                    else:
                        state.entity_direction = 2  # right
                else:
                    if distance_to_agent[0] < 0:
                        state.entity_direction = 1  # up
                    else:
                        state.entity_direction = 3  # down
                if not Walk.action(state):
                    if zombie_direction == 1:   # up
                        object_in_front_coordinate = [self.position[0] - 1][self.position[1]]
                    elif zombie_direction == 2: # right
                        object_in_front_coordinate = [self.position[0]][self.position[1] + 1]
                    elif zombie_direction == 3: # down
                        object_in_front_coordinate = [self.position[0] + 1][self.position[1]]
                    else:   # left
                        object_in_front_coordinate = [self.position[0]][self.position[1] - 1]
                    object_in_front = state.map_grid[object_in_front_coordinate]
                    object_in_front.durability -= 1
                    if object_in_front.durability <= 0:
                        state.map_grid[object_in_front_coordinate] = Ground()
        state.zombie = None  # Clear the zombie from the state after action is taken