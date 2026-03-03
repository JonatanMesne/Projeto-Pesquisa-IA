from entities.agent import Agent
from entities.zombie import Zombie
from actions.action import Action
from world import World

class State:
    def __init__(self):
        self.entity_direction = 0  # 1 (up) | 2 (right) | 3 (down) | 4 (left)
        self.agent: Agent
        self.zombies = []
        self.action_zombie: Zombie | None = None  # Store the current zombie in the state for access in actions
        self.world: World
        self.current_action: Action | None = None
        self.time_elapsed = 0
        self.index = -1
        self.hunger_per_time = 3
        self.thirst_per_time = 3
        self.stamina_per_time = 5
        self.hunger_damage = 3
        self.thirst_damage = 3
        self.bleeding_damage = 6
        self.hunger_threshold = 80
        self.thirst_threshold = 80
        self.wave_count = 0
        self.time_limit = 1000
        self.zombies_killed = 0
        
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
        self.current_action = None
        self.time_elapsed = 0
        self.index = -1
        self.wave_count = 0
        self.time_limit = time_limit
        
        self.world.generate_map(self, seed=seed)
        
    def environment_start(self):
        while self.time_elapsed < self.time_limit:
            no_valid_action = True
            while no_valid_action:
                no_valid_action = False
                if self.agent.choose_action(self) == False:
                    no_valid_action = True
            self.advance_time()
            if self.agent.health <= 0:
                print("Game over")
                break
        print(f"You survived for {self.time_elapsed} time units.")
            
                    
            
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
        return self.world.grid[WO_position[0]][WO_position[1]]
    
    def advance_time(self):
        action_duration = self.current_action.duration # type: ignore
        self.current_action.action(self)    # type: ignore
        for _ in range(action_duration):
            self.time_elapsed += 1
            for zombie in self.zombies:
                zombie.zombie_action(self)
            if self.agent.health <= 0:
                print("You died of a zombie attack.")
                break
                
            #status handler (status, hunger, thirst)
            self.agent.hunger = min(self.agent.max_hunger, self.agent.hunger + self.hunger_per_time)
            self.agent.thirst = min(self.agent.max_thirst, self.agent.thirst + self.thirst_per_time)
            #apply status, then check if status is done, then add new status
            if self.agent.hunger >= self.hunger_threshold and "hungry" not in self.agent.status:
                self.agent.status.append("hungry")
            if self.agent.thirst >= self.thirst_threshold and "thirsty" not in self.agent.status:
                self.agent.status.append("thirsty")
            if self.agent.stamina <= 0 and "tired" not in self.agent.status:
                self.agent.status.append("tired")
                
            if "hungry" not in self.agent.status and "thirsty" not in self.agent.status:
                self.agent.stamina = min(self.agent.max_stamina, self.agent.stamina + self.stamina_per_time)
                
            if "hungry" in self.agent.status:
                self.agent.health -= self.hunger_damage
                print("You are dying of hunger.")
                if self.agent.health <= 0:
                    print("You died of hunger.")
                    break
            if "thirsty" in self.agent.status:
                self.agent.health -= self.thirst_damage
                print("You are dying of thirst.")
                if self.agent.health <= 0:
                    print("You died of thirst.")
                    break
            if "bleeding" in self.agent.status:
                self.agent.health -= self.bleeding_damage
                print("You are bleeding to death.")
                if self.agent.health <= 0:
                    print("You died of bleeding.")
                    break
            if "tired" in self.agent.status and self.agent.stamina > 30:
                self.agent.status.remove("tired")
            
            #wave handler
            if len(self.zombies) < self.world.wave_size * self.wave_count * 0.2:
                self.wave_count += 1
                self.world.generate_wave(self)
        
    def entity_death(self, entity):
        self.world.grid[entity.position[0]][entity.position[1]] = entity.standing_on
        if isinstance(entity, Zombie):
            self.zombies.remove(entity)
            self.zombies_killed += 1