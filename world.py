import random
from chunks import Chunk
from entities.zombie import Zombie
from buildings import Buildings
from world_objects.ground import Ground

from items.item import Item
from items.ammo import Ammo
from items.medkit import Medkit
from items.food import Food
from items.water import Water
from items.weapons.baseball_bat import BaseballBat
from items.weapons.knife import Knife
from items.weapons.pistol import Pistol
from items.weapons.smg import Smg

class World:
    def __init__(self, map_length = 4, map_height = 4, wave_size = 20):
        self.length = map_length
        self.height = map_height
        self.grid = []
        self.seed = ''
        self.seed_pointer = 0
        self.wave_size = wave_size
        self.item_chance = 15
        
    def generate_seed(self):
        for _ in range(16):
            self.seed += str(random.randint(0, 9))
    
    def generate_new_seed(self):
        new_seed = ''
        for i in range(0, len(self.seed), 4):
            seed_number = int(self.seed[i:i+4]) + 1     #add 1 in case the number is 0
            seed_number = str(seed_number * 47629)   #multiply with a prime number
            if len(seed_number) > 4:
                seed_number = int(seed_number[1:5])   #get the digits 1 to 4 (the digit 0 keeps repeating a pattern, so it isn't used)
            else:
                seed_number = int(seed_number)
                
            magnitude = 1000
            while seed_number < magnitude and magnitude > 1:
                new_seed += '0'
                magnitude /= 10
                
            new_seed += str(seed_number)
            
        self.seed_pointer = 0
        self.seed = new_seed
        
    #upper limit not inclusive
    def get_seed_number(self, digits, upper_limit = 0) -> int:        
        return_value = ''
        while True:
            seed_number = self.seed[self.seed_pointer:self.seed_pointer + digits]
            return_value += seed_number
            if len(seed_number) < digits:
                self.generate_new_seed()
                digits -= len(seed_number)
            else:
                self.seed_pointer += digits
                return_value = int(return_value)
                if upper_limit > 0:
                    return_value = return_value % upper_limit
                return return_value
    
    def generate_buildings(self):
        for i in range(self.height):
            for j in range(self.length):
                buildingNumber = self.get_seed_number(2, 3)
                houseType = ''
                if i % 2 == 0:
                    if j % 2 == 0:
                        houseType = 'A'
                    else:
                        houseType = 'B'
                else:
                    if j % 2 == 0:
                        houseType = 'C'
                    else:
                        houseType = 'D'
                
                # types = ['A', 'B', 'C', 'D']
                
                # houseType = random.choice(types)
                        
                if houseType == 'A':
                    if buildingNumber == 0:
                        Buildings.house1A(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2A(self, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3A(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
                    
                if houseType == 'B':
                    if buildingNumber == 0:
                        Buildings.house1B(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2B(self, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3B(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
                
                if houseType == 'C':
                    if buildingNumber == 0:
                        Buildings.house1C(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2C(self, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3C(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
                        
                if houseType == 'D':
                    if buildingNumber == 0:
                        Buildings.house1D(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2D(self, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3D(self, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
        self.place_items()
        
    def place_items(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if isinstance(self.grid[i][j], Item):
                    item = self.choose_item()
                    self.grid[i][j] = item
            
    def choose_item(self, item_chance = None):
        if(item_chance == None):
            item_chance = self.item_chance
        item_array = [Ammo, Ammo, Medkit, Medkit, Food, Food, Water, Water, BaseballBat, Knife, Pistol, Smg]
        seed_number = self.get_seed_number(2, 100)
        if seed_number > item_chance:
            return Ground()
        else:
            seed_number = seed_number % len(item_array)
            return item_array[seed_number]()
        
                        
    def generate_wave(self, state):
        for _ in range(self.wave_size):
            zombie = Zombie()
            zombie.place_zombie(self, state.agent)
            state.zombies.append(zombie)
        

    def generate_map(self, state, seed = None):
        if(seed == None):
            self.generate_seed()
        else: #check seed
            self.seed = ''
            for number in seed:
                if number >= '0' and number <= '9':
                    self.seed += number
            if len(self.seed) == 0:
                self.generate_seed()
            
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSeed:", self.seed)
        
        #extracting starting coordinates for agent from seed
        agent_x = self.get_seed_number(3, self.height * Chunk.chunk_size)
        agent_y = self.get_seed_number(3, self.length * Chunk.chunk_size)
        
        self.grid = []
        for _ in range(self.height * Chunk.chunk_size):
            self.grid.append([])

        for i in range(self.height):
            for _ in range(self.length):
                Chunk.create_empty_chunk(self.grid, i*Chunk.chunk_size)
                
        self.generate_buildings()
                
        # placing agent in the map
        state.agent.place_entity(self.grid, [agent_x, agent_y])
        
        self.generate_wave(state)
            
    def __str__(self) -> str:
        grid = ''
        # for i in range(self.length * Chunk.chunk_size):
        #     grid += str(i + 1) + ' '
        # grid += '\n'
        for i in range(self.height * Chunk.chunk_size):
            # grid += str(i + 1) + ' '
            for j in range(self.length * Chunk.chunk_size):
                grid += self.grid[i][j].appearence + ' '
            grid += '\n'
        return grid