from actions.idle import Idle
from actions.walk import Walk
from actions.run import Run
from actions.attack import Attack
from actions.climb import Climb
from actions.door_action import DoorAction
from actions.item_actions.drink import Drink
from actions.item_actions.eat import Eat
from actions.item_actions.heal import Heal
from actions.item_actions.reload import Reload
from actions.item_actions.unload import Unload
from actions.pickup_item import PickupItem
from actions.change_held_item import ChangeHeldItem
from actions.drop_item import DropItem
from actions.action import Action

from actions.update_vision import UpdateVision
from entities.agent import Agent
from entities.zombie import Zombie
from actions.action import Action
from actions.update_vision import UpdateVision
from world import World

class State:
    all_possible_agent_actions_ids = [
        0,  #idle
        1,  #walk up
        2,  #walk right
        3,  #walk down
        4,  #walk left
        5,  #run up
        6,  #run right
        7,  #run down
        8,  #run left
        9,  #attack up
        10,  #attack right
        11,  #attack down
        12,  #attack left
        13,  #climb up
        14,  #climb right
        15,  #climb down
        16,  #climb left
        17,  #door_action up
        18,  #door_action right
        19,  #door_action down
        20,  #door_action left
        21,  #drink
        22,  #eat
        23,  #heal
        24,  #reload
        25,  #unload
        26  #pickup_item
    ]
    for i in range(100, 100 + Agent.max_inventory_space):   #adding change_held_item ids for every inventory slot
        all_possible_agent_actions_ids.append(i)
    for i in range(200, 200 + Agent.max_inventory_space):   #adding drop_item ids for every inventory slot
        all_possible_agent_actions_ids.append(i)
        
    all_possible_agent_actions = [
        Idle, 
        Walk, 
        Run, 
        Attack, 
        Climb, 
        DoorAction, 
        Drink, 
        Eat, 
        Heal, 
        Reload, 
        Unload, 
        PickupItem,
        ChangeHeldItem,
        DropItem,
        Action
    ]
    
    def get_action(self, action_id):
        for i in range(len(self.all_possible_agent_actions)):
            if action_id < self.all_possible_agent_actions[i].id:
                return self.all_possible_agent_actions[i-1]
        return None #should never reach this
    
    def __init__(self):
        self.agent: Agent
        self.zombies = []
        # self.zombies_vectors = []
        self.action_zombie: Zombie | None = None  # Store the current zombie in the state for access in actions
        self.world: World
        self.current_action_id = -1
        self.time_elapsed = 0
        self.hunger_per_time = 1
        self.thirst_per_time = 1
        self.stamina_per_time = 5
        self.hunger_damage = 3
        self.thirst_damage = 3
        self.bleeding_damage = 6
        self.hunger_threshold = 80
        self.thirst_threshold = 80
        self.wave_count = 0
        self.time_limit = 1000
        self.zombies_killed = 0
        self.vector = []
        # self.vector = [self.agent.vector, self.world.vector, self.time_elapsed, self.hunger_per_time, self.thirst_per_time,
        #                self.stamina_per_time, self.hunger_damage, self.thirst_damage, self.bleeding_damage,
        #                self.hunger_threshold, self.thirst_threshold, self.wave_count, self.time_limit, self.zombies_killed,
        #                self.zombies_vectors]

    def update_vector(self):
        self.agent.update_vector()
        self.zombies_vectors = []
        for zombie in self.zombies:
            zombie.update_vector()
            self.zombies_vectors.append(zombie.vector)
        self.world.update_vector()
        self.vector = [self.agent.vector, self.world.vector, self.time_elapsed, self.hunger_per_time, self.thirst_per_time,
                       self.stamina_per_time, self.hunger_damage, self.thirst_damage, self.bleeding_damage,
                       self.hunger_threshold, self.thirst_threshold, self.wave_count, self.time_limit, self.zombies_killed]
        # self.vector.append(self.zombies_vectors)
        
    def print_self(self):
        print("Agent Direction:", self.entity_direction)
        print("Map Grid:")
        for row in self.world.grid:
            print(' '.join(row.appearence for row in row))
    
    def reset(self, seed=None, player_controlled=False, time_limit=1000):
        self.entity_direction = 0
        self.agent = Agent(player_controlled=player_controlled)
        self.zombies = []
        self.action_zombie = None
        self.world = World()
        self.current_action_id = -1
        self.time_elapsed = 0
        self.index = -1
        self.wave_count = 0
        self.time_limit = time_limit
        
        self.world.generate_map(self, seed=seed)
        
    def environment_start(self):
        while self.time_elapsed < self.time_limit:
            no_valid_action = True
            UpdateVision().action(self)
            while no_valid_action:
                no_valid_action = False
                if self.agent.choose_action(self) == False:
                    no_valid_action = True
            print(f"Reward: {self.advance_time()}") 
            if self.agent.health <= 0:
                print("Game over")
                break
        print(f"You survived for {self.time_elapsed} time units.")
            
    def get_world_object_in_front(self, direction):
        WO_position = self.agent.position.copy()
        #direction = 0 (up) | 1 (right) | 2 (down) | 3 (left)
        if direction == 0:
            WO_position[0] -= 1
        elif direction == 1:
            WO_position[1] += 1
        elif direction == 2:
            WO_position[0] += 1
        elif direction == 3:
            WO_position[1] -= 1
        if (WO_position[0] < 0 or WO_position[0] >= len(self.world.grid) or
        WO_position[1] < 0 or WO_position[1] >= len(self.world.grid[0])):
            return None
        return self.world.grid[WO_position[0]][WO_position[1]]
    
    def advance_time(self) -> int:
        reward = 0
        current_action = self.get_action(self.current_action_id)
        action_duration = current_action.duration # type: ignore
        reward = current_action.action(self) # type: ignore
        if reward == -100:
            return reward       #?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????/
        
        oldAgentHealth = self.agent.health
        oldZombiesKilled = self.zombies_killed
        
        for _ in range(action_duration):
            self.time_elapsed += 1
            for zombie in self.zombies:
                zombie.zombie_action(self)
            if self.agent.health <= 0:
                print("You died of a zombie attack.")
                reward += self.entity_death(self.agent)
                
            #status handler (status, hunger, thirst)
            self.agent.hunger = min(self.agent.max_hunger, self.agent.hunger + self.hunger_per_time)
            self.agent.thirst = min(self.agent.max_thirst, self.agent.thirst + self.thirst_per_time)
            #apply status, then check if status is done, then add new status
            # agentStatus = [
            #     0, thirsty
            #     0, hungry
            #     0, bleeding
            #     0  tired
            # ]
            if self.agent.hunger >= self.hunger_threshold:
                self.agent.status[1] = 1
            if self.agent.thirst >= self.thirst_threshold:
                self.agent.status[0] = 1
            if self.agent.stamina <= 0:
                self.agent.status[3] = 1
                
            if self.agent.status[0] == 0 and self.agent.status[1] == 0:
                self.agent.stamina = min(self.agent.max_stamina, self.agent.stamina + self.stamina_per_time)
                
            if self.agent.status[1] == 1:
                self.agent.health -= self.hunger_damage
                print("You are dying of hunger.")
                if self.agent.health <= 0:
                    print("You died of hunger.")
                    reward += self.entity_death(self.agent)
            if self.agent.status[0] == 1:
                self.agent.health -= self.thirst_damage
                print("You are dying of thirst.")
                if self.agent.health <= 0:
                    print("You died of thirst.")
                    reward += self.entity_death(self.agent)
            if self.agent.status[2] > 0:
                self.agent.health -= self.bleeding_damage
                self.agent.status[2] -= 1
                print("You are bleeding to death.")
                if self.agent.health <= 0:
                    print("You died of bleeding.")
                    reward += self.entity_death(self.agent)
            if self.agent.stamina > 30:
                self.agent.status[3] = 0
            
            #wave handler
            if len(self.zombies) < self.world.wave_size * self.wave_count * 0.2:
                self.wave_count += 1
                self.world.generate_wave(self)
                
        reward += (self.agent.health - oldAgentHealth) * 0.5
        reward += (self.zombies_killed - oldZombiesKilled) * 10
        reward -= self.agent.status[0] * 10  #thirsty
        reward -= self.agent.status[1] * 10  #hungry
        reward -= self.agent.status[2] * 20  #bleeding
        reward -= self.agent.status[3] * 5  #tired
        return reward
        
    def entity_death(self, entity) -> int:
        if entity.__class__.__name__ == "Zombie":
            entity.zombie_death(self)
            self.world.grid[entity.position[0]][entity.position[1]] = entity.standing_on
            return 0
        elif entity.__class__.__name__ == "Agent":
            return -1000
        return 1
        