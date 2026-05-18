import random

from actions.climb import Climb
from actions.idle import Idle
from actions.item_actions.drink import Drink
from actions.item_actions.eat import Eat
from actions.item_actions.heal import Heal
from actions.item_actions.reload import Reload
from actions.run import Run
from actions.update_vision import UpdateVision
from entities.entity import Entity
from world_objects.world_object import WorldObject
from actions.walk import Walk
from actions.attack import Attack 
from actions.pickup_item import PickupItem

from items.item import Item
from items.water import Water
from items.food import Food
from items.medkit import Medkit
from items.ammo import Ammo

class Agent(Entity):
    id = 1
    max_inventory_qtt = [3, 2, 3, 3]   #max qtt for each type of item in inventory (ammo, medkits, food, water)
    possible_status_effects = ["thirsty", "hungry", "tired", "bleeding"]

    #construtor
    def __init__(self, player_controlled = False):
        super().__init__('A', 100, vision_range=4)
        self.inventory_qtt = [0, 0, 0, 0]   #ammo, medkits, food, water
        self.inventory = []   #list of item objects in inventory
        self.melee_weapon = None
        self.ranged_weapon = None
        self.inventory_space_used = 0
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.max_health = 100
        self.max_hunger = 100
        self.hunger = 0
        self.max_thirst = 100
        self.thirst = 0
        self.status = [0, 0, 0, 0]   #binary vector indicating whether the agent is affected by each possible status effect
        self.player_controlled = player_controlled
        self.possible_actions = []
        
    def find_item_in_inventory(self, item_id):
        for item in self.inventory:
            if item.id == item_id:
                return item
        return None
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
                print(f"- Bleeding (Loses health over time)")
            if self.status[3] > 0:
                print(f"- Tired (Cannot run or climb)")
        else:
            print("Status Effects: None")
        print(f"Standing on: {self.standing_on.__class__.__name__ if self.standing_on else 'None'}")
        
    def print_inventory(self):
        print(f"Inventory Quantity: {self.inventory_qtt}/{self.max_inventory_qtt}")
        print("\nInventory:")
        if len(self.inventory) == 0:
            print("Inventory is empty.")
        else:
            for item in self.inventory:
                item.print_info()
        print(f"\nMelee Weapon: {self.melee_weapon.__class__.__name__ if self.melee_weapon else 'Fists'}")
        print(f"Ranged Weapon: {self.ranged_weapon.__class__.__name__ if self.ranged_weapon else 'None'}")
            
    def update_possible_actions(self, state):
        self.possible_actions = []
        
        if self.stamina + Idle.stamina_recovery < self.max_stamina:
            self.possible_actions.append(Idle.id)
        
        #world object dependent actions
        world_objects = []
        #if up is a valid position
        if self.position[0] - 1 >= 0:
            world_objects.append(state.world.grid[self.position[0] - 1][self.position[1]])
            self.possible_actions.append(Attack.id + 0)
            if self.ranged_weapon is not None and self.ranged_weapon.ammo > 0:
                self.possible_actions.append(Attack.id + 4)
        else:
            world_objects.append(None)
        #if right is a valid position
        if self.position[1] + 1 < len(state.world.grid[0]):
            world_objects.append(state.world.grid[self.position[0]][self.position[1] + 1])
            self.possible_actions.append(Attack.id + 1)
            if self.ranged_weapon is not None and self.ranged_weapon.ammo > 0:
                self.possible_actions.append(Attack.id + 5)
        else:
            world_objects.append(None)
        #if down is a valid position
        if self.position[0] + 1 < len(state.world.grid):
            world_objects.append(state.world.grid[self.position[0] + 1][self.position[1]])
            self.possible_actions.append(Attack.id + 2)
            if self.ranged_weapon is not None and self.ranged_weapon.ammo > 0:
                self.possible_actions.append(Attack.id + 6)
        else:
            world_objects.append(None)
        #if left is a valid position
        if self.position[1] - 1 >= 0:
            world_objects.append(state.world.grid[self.position[0]][self.position[1] - 1])
            self.possible_actions.append(Attack.id + 3)
            if self.ranged_weapon is not None and self.ranged_weapon.ammo > 0:
                self.possible_actions.append(Attack.id + 7)
        else:
            world_objects.append(None)
            
        for i in range(len(world_objects)):
            if isinstance(world_objects[i], WorldObject):
                if not world_objects[i].is_solid:
                    self.possible_actions.append(Walk.id + i)
                    if self.stamina >= Run.stamina_cost and self.status[3] == 0:
                        self.possible_actions.append(Run.id + i)
                if world_objects[i].has_action:
                    if isinstance(world_objects[i].action, Climb) and state.agent.stamina <= 10:
                        continue
                    self.possible_actions.append(world_objects[i].action.id + i)
        
        if isinstance(self.standing_on, Item):
            self.possible_actions.append(PickupItem.id)
            
        if self.inventory_qtt[1] > 0:
            self.possible_actions.append(Heal.id)
        if self.inventory_qtt[2] > 0:
            self.possible_actions.append(Eat.id)
        if self.inventory_qtt[3] > 0:
            self.possible_actions.append(Drink.id)
            
        if (self.ranged_weapon is not None and self.ranged_weapon.ammo < self.ranged_weapon.ammo_capacity
            and self.inventory_qtt[0] > 0):
            self.possible_actions.append(Reload.id)
                    
        self.possible_actions.sort()
                    
    def print_actions(self, state):
        print("\nPossible Actions:")
        for i in range(len(self.possible_actions)):
            action = state.get_action(self.possible_actions[i])
            if action.need_direction:
                direction = ""
                if (self.possible_actions[i] - action.id) % 4 == 0:
                    direction = "Up"
                elif (self.possible_actions[i] - action.id) % 4 == 1:
                    direction = "Right"
                elif (self.possible_actions[i] - action.id) % 4 == 2:
                    direction = "Down"
                elif (self.possible_actions[i] - action.id) % 4 == 3:
                    direction = "Left"
                if action.id == Attack.id:
                    if self.possible_actions[i] >= Attack.id + 4:
                        weapon = "ranged"
                    else:
                        weapon = "melee"
                    print(f"{self.possible_actions[i]}- {action.__name__} with {weapon} weapon (Direction: {direction})")
                else:
                    print(f"{self.possible_actions[i]}- {action.__name__} (Direction: {direction})")
            else:
                print(f"{self.possible_actions[i]}- {action.__name__}")
                
    def print_agent_info(self, state):
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
                    if choice not in self.possible_actions:
                        print("Invalid choice. Please enter a valid number.")
                    else:
                        state.current_action_id = choice
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    return True
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    # return False
        else:
            # choice = random.randint(0, len(self.possible_actions) - 1)
            # state.current_action_id = self.possible_actions[choice]
            choice = random.randint(0, len(state.all_possible_agent_actions_ids) - 1)
            state.current_action_id = state.all_possible_agent_actions_ids[choice]
            return True