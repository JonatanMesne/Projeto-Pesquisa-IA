import random

from actions.drop_item import DropItem
from actions.idle import Idle
from actions.run import Run
from actions.update_vision import UpdateVision
from entities.entity import Entity
from items.weapons.melee import MeleeWeapon
from items.weapons.ranged import RangedWeapon
from world_objects.world_object import WorldObject
from items.item import Item
from actions.walk import Walk
from actions.attack import Attack 
from actions.pickup_item import PickupItem
from actions.change_held_item import ChangeHeldItem

class Agent(Entity):
    max_inventory_space = 10   #max 100
    #construtor
    def __init__(self, appearence = 'A', health = 100, inventory = [], 
                status = [], vision_range = 6, player_controlled = False):
        super().__init__(appearence, health, vision_range)
        self.inventory = inventory
        self.max_inventory_space = Agent.max_inventory_space 
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
                
    def print_status(self, state):
        print(f"\nHealth: {self.health}/{self.max_health}")
        print(f"Stamina: {self.stamina}/{self.max_stamina} + {state.stamina_per_time} per time unit, if not hungry or thirsty")
        print(f"Hunger: {self.hunger}/{self.max_hunger} + {state.hunger_per_time} per time unit")
        print(f"Thirst: {self.thirst}/{self.max_thirst} + {state.thirst_per_time} per time unit")
        if len(self.status) > 0:
            print(f"Status Effects: {', '.join(self.status)}")
        else:
            print("Status Effects: None")
        print(f"Inventory Space Used: {self.inventory_space_used}/{self.max_inventory_space}")
        if isinstance(self.item_in_hand, RangedWeapon) or isinstance(self.item_in_hand, MeleeWeapon):
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
        self.possible_actions.append(Idle.id)
        
        #world object dependent actions
        world_objects = []
        #if up is a valid position
        if self.position[0] - 1 >= 0:
            world_objects.append(state.world.grid[self.position[0] - 1][self.position[1]])
            self.possible_actions.append(Attack.id + 0)
        else:
            world_objects.append(None)
        #if up is a valid position
        if self.position[1] + 1 < len(state.world.grid[0]):
            world_objects.append(state.world.grid[self.position[0]][self.position[1] + 1])
            self.possible_actions.append(Attack.id + 1)
        else:
            world_objects.append(None)
        #if up is a valid position
        if self.position[0] + 1 < len(state.world.grid):
            world_objects.append(state.world.grid[self.position[0] + 1][self.position[1]])
            self.possible_actions.append(Attack.id + 2)
        else:
            world_objects.append(None)
        #if up is a valid position
        if self.position[1] - 1 >= 0:
            world_objects.append(state.world.grid[self.position[0]][self.position[1] - 1])
            self.possible_actions.append(Attack.id + 3)
        else:
            world_objects.append(None)
            
        for i in range(len(world_objects)):
            if isinstance(world_objects[i], WorldObject):
                if not world_objects[i].isSolid:
                    self.possible_actions.append(Walk.id + i)
                    self.possible_actions.append(Run.id + i)
                if not isinstance(world_objects[i], Item):
                    if world_objects[i].has_action:
                        if world_objects[i].action.__name__ == 'Climb' and state.agent.stamina <= 10:
                            continue
                        self.possible_actions.append(world_objects[i].action.id + i)
        
        if isinstance(self.standing_on, Item):
            self.possible_actions.append(PickupItem.id)
        
        if len(self.inventory) > 0:
            if self.item_in_hand == None:
                for i in range(len(self.inventory)):
                    self.possible_actions.append(ChangeHeldItem.id + i)
            elif len(self.inventory) > 1:
                for i in range(len(self.inventory)):
                    self.possible_actions.append(ChangeHeldItem.id + i)
            for i in range(len(self.inventory)):
                self.possible_actions.append(DropItem.id + i)
            
        if self.item_in_hand != None:
            if self.item_in_hand.has_action: 
                for action in self.item_in_hand.action:  # type: ignore
                    if action.__name__ == 'Unload' and self.item_in_hand.ammo <= 0:  # type: ignore
                        continue
                    self.possible_actions.append(action.id)
                    
    def print_actions(self, state):
        print("\nPossible Actions:")
        for i in range(len(self.possible_actions)):
            action = state.get_action(self.possible_actions[i])
            if action.need_direction:
                direction = ""
                if self.possible_actions[i] - action.id == 0:
                    direction = "Up"
                elif self.possible_actions[i] - action.id == 1:
                    direction = "Right"
                elif self.possible_actions[i] - action.id == 2:
                    direction = "Down"
                elif self.possible_actions[i] - action.id == 3:
                    direction = "Left"
                print(f"{i}- {action.__name__} (Direction: {direction})")
            elif action.need_index:
                print(f"{i}- {action.__name__} (Index: {self.possible_actions[i] - action.id})")
            else:
                print(f"{i}- {action.__name__}")
                
    def print_agent_info(self, state):
        UpdateVision().action(state)
        self.print_vision_data()
        self.print_status(state)
        self.print_inventory()
        self.update_possible_actions(state)
        self.print_actions(state)
        
    def choose_action(self, state) -> bool:
        self.print_agent_info(state)
        if self.player_controlled:
            while True:
                try:
                    choice = int(input("\nEnter the number of the action you want to perform: "))
                    if choice < 0 or choice >= len(self.possible_actions):
                        print("Invalid choice. Please enter a valid number.")
                    else:
                        state.current_action_id = self.possible_actions[choice]
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    return True
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    # return False
        else:
            choice = random.randint(0, len(self.possible_actions) - 1)
            state.current_action_id = self.possible_actions[choice]
            return True