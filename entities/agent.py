from entities.entity import Entity
from world_objects.world_object import WorldObject
from items.item import Item
from actions.walk import Walk
from actions.item_actions.attack import Attack 
from actions.pickup_item import PickupItem
from actions.change_held_item import ChangeHeldItem

class Agent(Entity):
    #construtor
    def __init__(self, appearence = 'A', health = 100, inventory = [], max_inventory_space = 10, max_stamina = 10, 
                 stamina = 10, status = 0, vision_range = 6):
        super().__init__(appearence, health, vision_range)
        self.inventory = inventory
        self.max_inventory_space = max_inventory_space
        self.inventory_space_used = 0
        self.max_stamina = max_stamina
        self.stamina = stamina
        self.max_health = health
        self.status = status
        self.item_in_hand = None
    
    def print_inventory(self):
        print("Inventory:")
        if len(self.inventory) == 0:
            print("Inventory is empty.")
        else:
            for i in range(len(self.inventory)):
                item = self.inventory[i]
                print(f"{i}- {item.appearence}")
                
    def print_status(self):
        print(f"\nHealth: {self.health}/{self.max_health}")
        print(f"Stamina: {self.stamina}/{self.max_stamina}")
        print(f"Inventory Space Used: {self.inventory_space_used}/{self.max_inventory_space}")
        print(f"Item in Hand: {self.item_in_hand.appearence if self.item_in_hand else 'None'}")
        
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.inventory_space_used -= item.inventory_space
            
    def update_possible_actions(self, state):
        self.possible_actions = []
        
        # standard actions
        self.possible_actions.append(Walk)
        self.possible_actions.append(Attack)
        self.possible_actions.append(ChangeHeldItem)
        
        #world object actions
        world_objects = []
        if self.position[0] - 1 >= 0:
            world_objects.append(state.map_grid[self.position[0] - 1][self.position[1]])
        else:
            world_objects.append(None)
        if self.position[1] + 1 < len(state.map_grid[0]):
            world_objects.append(state.map_grid[self.position[0]][self.position[1] + 1])
        else:
            world_objects.append(None)
        if self.position[0] + 1 < len(state.map_grid):
            world_objects.append(state.map_grid[self.position[0] + 1][self.position[1]])
        else:
            world_objects.append(None)
        if self.position[1] - 1 >= 0:
            world_objects.append(state.map_grid[self.position[0]][self.position[1] - 1])
        else:
            world_objects.append(None)
        for i in range(len(world_objects)):
            if isinstance(world_objects[i], WorldObject):
                if world_objects[i].has_action:
                    self.possible_actions.append([world_objects[i].action, i+1])
                    
        if isinstance(self.standing_on, Item):
            self.possible_actions.append(PickupItem)
            
        if self.item_in_hand != None:
            if self.item_in_hand.has_action: 
                for action in self.item_in_hand.action:  # type: ignore
                    self.possible_actions.append(action)
                    
    def print_actions(self):
        print("\nPossible Actions:")
        for i in range(len(self.possible_actions)):
            action = self.possible_actions[i]
            if isinstance(action, list):
                direction = ""
                if action[1] == 1:
                    direction = "Up"
                elif action[1] == 2:
                    direction = "Right"
                elif action[1] == 3:
                    direction = "Down"
                elif action[1] == 4:
                    direction = "Left"
                print(f"{i}- {action[0].__name__} (Direction: {direction})")
            else:
                print(f"{i}- {action.__name__}")
                
        