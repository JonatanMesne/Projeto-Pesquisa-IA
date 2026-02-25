import random
from chunks import Chunk
from entities.agent import Agent
from buildings import Buildings

class World:
    length: int = 4   #measured in quantity of chunks
    height: int = 4    #measured in quantity of chunks
    
    def __init__(self, map_length = length, map_height = height):
        self.length = map_length
        self.height = map_height
        self.grid = []
        
    #00: starting x coordinate for agent
    #00: starting y coordinate for agent
    def generateSeed(self) -> str:
        starting_x = random.randint(0, self.length * Chunk.chunk_size - 1)
        if(starting_x < 10):
            starting_x = "0" + str(starting_x)
        else:
            starting_x = str(starting_x)

        starting_y = random.randint(0, self.height * Chunk.chunk_size - 1)
        if(starting_y < 10):
            starting_y = "0" + str(starting_y)
        else:
            starting_y = str(starting_y)
        
        seed = starting_x + starting_y
        return seed
    
    def generateBuildings(self):
        for i in range(self.height):
            for j in range(self.length):
                buildingNumber = random.randint(0, 2)
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
                        Buildings.house1A(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2A(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3A(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
                    
                if houseType == 'B':
                    if buildingNumber == 0:
                        Buildings.house1B(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2B(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3B(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
                
                if houseType == 'C':
                    if buildingNumber == 0:
                        Buildings.house1C(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2C(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3C(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")
                        
                if houseType == 'D':
                    if buildingNumber == 0:
                        Buildings.house1D(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    elif buildingNumber == 1:
                        Buildings.house2D(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)    
                    elif buildingNumber == 2:
                        Buildings.house3D(self, 0, i * Chunk.chunk_size, j * Chunk.chunk_size)
                    else:
                        print("Number out of range")

    def generateMap(self, agent : Agent, seed = None):
        if(seed == None):
            seed = self.generateSeed()
            
        #extracting starting coordinates for agent from seed
        starting_x = int(seed[0:2])
        starting_y = int(seed[2:4])
        
        self.grid = []
        for _ in range(self.height * Chunk.chunk_size):
            self.grid.append([])

        for i in range(self.height):
            for _ in range(self.length):
                Chunk.createEmptyChunk(self.grid, i*Chunk.chunk_size)
                
        # placing agent in the map
        while True:
            sum_for_x = 1
            sum_for_y = 1
            if(self.grid[starting_x][starting_y].is_solid):
                if(starting_x == self.length * Chunk.chunk_size - 1):
                    sum_for_x = -1
                elif(starting_x == 0):
                    sum_for_x = 1
                starting_x += sum_for_x
            if(self.grid[starting_x][starting_y].is_solid):
                if(starting_y == self.length * Chunk.chunk_size - 1):
                    sum_for_y = -1
                elif(starting_x == 0):
                    sum_for_y = 1
                starting_y += sum_for_y
            else:
                agent.place_entity(self.grid, [starting_x, starting_y])
                break
        # for i in range(1):
        #     test_zombie = Zombie()
        #     test_zombie.place_entity(self.grid, [starting_x, starting_y + 1 + i])
        # self.grid[starting_x][starting_y + 3] = Wall()
            
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