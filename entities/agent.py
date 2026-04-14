import random

from actions.drop_item import DropItem
from actions.idle import Idle
from actions.run import Run
from actions.update_vision import UpdateVision
from entities.entity import Entity
from actions.walk import Walk
from actions.attack import Attack 
from actions.pickup_item import PickupItem
from actions.change_held_item import ChangeHeldItem

class Agent(Entity):
    id = 1
    possible_status_effects = ["thirsty", "hungry", "tired", "bleeding"]
    #construtor
    def __init__(self, appearence = 'A', health = 100, inventory = [], max_inventory_space = 10, 
                status = [0, 0, 0, 0], vision_range = 6, player_controlled = False):
        super().__init__(appearence, health, vision_range)
        self.inventory = inventory
        self.id_inventory = []
        self.max_inventory_space = max_inventory_space
        self.inventory_space_used = 0
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.max_health = health
        self.max_hunger = 100
        self.hunger = 0
        self.max_thirst = 100
        self.thirst = 0
        self.status = status
        self.item_in_hand = None
        self.player_controlled = player_controlled
        self.possible_actions = []
        
    vector = []
    # self.vector = [self.id_vision_data, self.position, self.standing_on.id, self.health, self.max_health, self.stamina, self.max_stamina, 
    #                self.hunger, self.max_hunger, self.thirst, self.max_thirst, self.status, self.id_inventory, self.inventory_space_used, 
    #                self.max_inventory_space, self.item_in_hand.id if self.item_in_hand else -1, self.possible_actions]

    def update_vector(self):
        self.vector = [self.id_vision_data, self.position, self.standing_on.id, self.health, self.max_health, self.stamina, self.max_stamina, 
                        self.hunger, self.max_hunger, self.thirst, self.max_thirst, self.status, self.id_inventory, self.inventory_space_used, 
                        self.max_inventory_space, self.item_in_hand.id if self.item_in_hand else -1, self.possible_actions]
        
    def sum_status(self) -> int:
        total = 0
        for i in range(len(self.status)):
            total += self.status[i]
        return total
                
    def print_status(self, state):
        print(f"\nHealth: {self.health}/{self.max_health}")
        print(f"Stamina: {self.stamina}/{self.max_stamina} + {state.stamina_per_time} per time unit, if not hungry or thirsty")
        print(f"Hunger: {self.hunger}/{self.max_hunger} + {state.hunger_per_time} per time unit")
        print(f"Thirst: {self.thirst}/{self.max_thirst} + {state.thirst_per_time} per time unit")
        if self.sum_status() > 0:
            print(f"Status Effects: ")
            if self.status[0] > 0:
                print(f"- Thirsty (Decreases stamina regeneration)")
            if self.status[1] > 0:
                print(f"- Hungry (Decreases stamina regeneration)")
            if self.status[2] > 0:
                print(f"- Tired (Cannot run or climb)")
            if self.status[3] > 0:
                print(f"- Bleeding (Loses health over time)")
        else:
            print("Status Effects: None")
        print(f"Inventory Space Used: {self.inventory_space_used}/{self.max_inventory_space}")
        if self.item_in_hand.__class__.__name__ == 'RangedWeapon' or self.item_in_hand.__class__.__name__ == 'MeleeWeapon':
            print(f"Item in Hand: {self.item_in_hand.detailed_item_info()}")
        else:
            print(f"Item in Hand: {self.item_in_hand.item_info() if self.item_in_hand else 'None'}")
        
    def print_inventory(self):
        print("\nInventory:")
        if len(self.inventory) == 0:
            print("Inventory is empty.")
        else:
            for i in range(len(self.inventory)):
                item = self.inventory[i]
                print(f"{i}- {item.item_info()}")
            
    def update_possible_actions(self, state):
        self.possible_actions = []
        
        # standard actions
        self.possible_actions.append(Idle)
        self.possible_actions.append(Walk)
        if "tired" not in self.status:
            self.possible_actions.append(Run)
        self.possible_actions.append(Attack)
        
        if len(self.inventory) > 0:
            if self.item_in_hand == None:
                self.possible_actions.append(ChangeHeldItem)    
            elif len(self.inventory) > 1:
                self.possible_actions.append(ChangeHeldItem)
            self.possible_actions.append(DropItem)
        
        #world object actions
        world_objects = []
        if self.position[0] - 1 >= 0:
            world_objects.append(state.world.grid[self.position[0] - 1][self.position[1]])
        else:
            world_objects.append(None)
        if self.position[1] + 1 < len(state.world.grid[0]):
            world_objects.append(state.world.grid[self.position[0]][self.position[1] + 1])
        else:
            world_objects.append(None)
        if self.position[0] + 1 < len(state.world.grid):
            world_objects.append(state.world.grid[self.position[0] + 1][self.position[1]])
        else:
            world_objects.append(None)
        if self.position[1] - 1 >= 0:
            world_objects.append(state.world.grid[self.position[0]][self.position[1] - 1])
        else:
            world_objects.append(None)
        for i in range(len(world_objects)):
            if world_objects[i].__class__.__name__ == 'WorldObject' and world_objects[i].__class__.__name__ != 'Item':
                if world_objects[i].has_action:
                    if world_objects[i].action.__name__ == 'Climb' and state.agent.stamina <= 10:
                        continue
                    self.possible_actions.append([world_objects[i].action, i+1])
                    
        if self.standing_on.__class__.__name__ == 'Item':
            self.possible_actions.append(PickupItem)
            
        if self.item_in_hand != None:
            if self.item_in_hand.has_action: 
                for action in self.item_in_hand.action:  # type: ignore
                    if action.__name__ == 'Unload' and self.item_in_hand.ammo <= 0:  # type: ignore
                        continue
                    if action.__name__ == 'Reload':
                        if self.item_in_hand.ammo >= self.item_in_hand.ammo_capacity:  # type: ignore
                            continue
                        else:
                            adicionar = False
                            for item in self.inventory:
                                if item.__class__.__name__ == 'Ammo':  # type: ignore
                                    adicionar = True
                                    break
                            if adicionar:
                                self.possible_actions.append(action)
                                continue
                    
                    self.possible_actions.append(action)
                    
    def print_actions(self):
        print("\nPossible Actions:")
        for i in range(len(self.possible_actions)):
            action = self.possible_actions[i]
            if action.__class__.__name__ == 'list':
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
                
    def print_agent_info(self, state):
        self.print_vision_data()
        self.print_status(state)
        self.print_inventory()
        self.update_possible_actions(state)
        self.print_actions()
        
    def choose_action(self, state) -> bool:
        self.print_agent_info(state)
        if self.player_controlled:
            while True:
                try:
                    choice = int(input("\nEnter the number of the action you want to perform: "))
                    if choice < 0 or choice >= len(self.possible_actions):
                        print("Invalid choice. Please enter a valid number.")
                    else:
                        if self.possible_actions[choice].__class__.__name__ == 'list':
                            state.current_action = self.possible_actions[choice][0]
                            if state.current_action.need_direction:
                                state.entity_direction = self.possible_actions[choice][1]
                            if state.current_action.need_index:
                                state.index = self.possible_actions[choice][1]
                        else:
                            state.current_action = self.possible_actions[choice]
                            if state.current_action.need_direction:
                                direction_choice = int(input("\nEnter the direction (1-Up, 2-Right, 3-Down, 4-Left): "))
                                if direction_choice < 1 or direction_choice > 4:
                                    print("Invalid direction. Please enter a valid number.")
                                    continue
                                else:
                                    state.entity_direction = direction_choice
                            if state.current_action.need_index:
                                index_choice = int(input("\nEnter the index: "))
                                if index_choice < 0:
                                    print("Invalid index. Please enter a valid number.")
                                    continue
                                else:
                                    state.index = index_choice
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    return True
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    return False
        else:
            choice = random.randint(0, len(self.possible_actions) - 1)
            if self.possible_actions[choice].__class__.__name__ == 'list':
                state.current_action = self.possible_actions[choice][0]
                if state.current_action.need_direction:
                    state.entity_direction = self.possible_actions[choice][1]
                if state.current_action.need_index:
                    state.index = self.possible_actions[choice][1]
            else:
                state.current_action = self.possible_actions[choice]
                if state.current_action.need_direction:
                    direction_choice = random.randint(1, 4)
                    state.entity_direction = direction_choice
                if state.current_action.need_index:
                    index_choice = random.randint(0, len(self.inventory) - 1)
                    state.index = index_choice
            return True