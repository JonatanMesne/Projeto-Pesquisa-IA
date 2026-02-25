from world_objects.door import Door
from world_objects.ground import Ground
from world_objects.small_wall import SmallWall
from world_objects.wall import Wall
from world_objects.world_object import WorldObject

class Chunk:
    chunk_size = 8
        
    @staticmethod
    def createEmptyChunk(map, chunk_x):
        for i in range(Chunk.chunk_size):
            for j in range(Chunk.chunk_size):
                map[chunk_x].append(Ground())
            chunk_x += 1
            
        