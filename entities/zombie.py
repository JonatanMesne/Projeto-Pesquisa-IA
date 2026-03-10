from entities.entity import Entity
from actions.update_vision import UpdateVision
from actions.walk import Walk
from entities.agent import Agent
from world_objects.ground import Ground
from world_objects.world_object import WorldObject
import random

class Zombie(Entity):
    min_distance_to_agent = 8
    #construtor
    def __init__(self, appearence = 'Z', health = 20, vision_range = 3, damage = 5):
        super().__init__(appearence, health, vision_range)
        self.damage = damage
        
    def print_status(self):
        print(f'Health: {self.health}')
        
    def place_zombie(self, world, agent):
        position = [world.get_seed_number(3, len(world.grid)), world.get_seed_number(3, len(world.grid[0]))]
        if world.grid[position[0]][position[1]].is_solid:
            position = self.find_open_space(world.grid, position)
            
        distance_to_agent = [abs(position[0] - agent.position[0]), abs(position[1] - agent.position[1])]
        if distance_to_agent[0] + distance_to_agent[1] > self.min_distance_to_agent:
            self.standing_on = world.grid[position[0]][position[1]]
            world.grid[position[0]][position[1]] = self
            self.position = position
        else:
            self.place_zombie(world, agent)
        
    def zombie_action(self, state):
        # Behavior logic for the zombie
        state.action_zombie = self  # Store the zombie in the state for access in actions
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
            # state.entity_direction = random.randint(1, 4)
            state.entity_direction = state.world.get_seed_number(1, 4) + 1 # Random direction if agent is not in vision
        if abs(distance_to_agent[0]) + abs(distance_to_agent[1]) == 1:
            # Attack the agent
            state.agent.health -= self.damage
            # random_number = random.randint(1, 100)
            random_number = state.world.get_seed_number(2, 100) + 1
            if random_number <= 20 and "bleeding" not in state.agent.status:
                state.agent.status.append("bleeding")
        else:
            zombie_direction = state.entity_direction
            if not Walk.action(state):
                if zombie_direction == 1 or zombie_direction == 3:
                    if distance_to_agent[1] < 0:
                        state.entity_direction = 4  # left
                    elif distance_to_agent[1] > 0:
                        state.entity_direction = 2  # right
                else:
                    if distance_to_agent[0] < 0:
                        state.entity_direction = 1  # up
                    elif distance_to_agent[0] > 0:
                        state.entity_direction = 3  # down
                if state.entity_direction == 0 or not Walk.action(state):
                    # determine coordinates in front of the zombie based on its original direction
                    if zombie_direction == 1:   # up
                        new_x = self.position[0] - 1
                        new_y = self.position[1]
                    elif zombie_direction == 2: # right
                        new_x = self.position[0]
                        new_y = self.position[1] + 1
                    elif zombie_direction == 3: # down
                        new_x = self.position[0] + 1
                        new_y = self.position[1]
                    else:   # left
                        new_x = self.position[0]
                        new_y = self.position[1] - 1

                    # only attempt to damage something if the coordinate is within the world bounds
                    max_x = len(state.world.grid)
                    max_y = len(state.world.grid[0])
                    if 0 <= new_x < max_x and 0 <= new_y < max_y:
                        object_in_front = state.world.grid[new_x][new_y]
                        if isinstance(object_in_front, WorldObject):
                            object_in_front.durability -= 1
                            if object_in_front.durability <= 0:
                                state.world.grid[new_x][new_y] = Ground()
                    # if the cell is outside the map we simply do nothing
        state.action_zombie = None  # Clear the zombie from the state after action is taken