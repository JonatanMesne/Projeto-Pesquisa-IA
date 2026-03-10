from chunks import Chunk
from world_objects.ground import Ground
from world_objects.door import Door
from world_objects.wall import Wall
from world_objects.fence import Fence

from items.item import Item

class Buildings:
    # W W W W W W W _
    # W i _ W _ i W _
    # W _ _ W _ _ W _
    # W _ i W i _ W _
    # W D W W W D W _
    # F _ _ F _ _ F _
    # F _ _ F _ _ F _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house1A(world, x, y):
        world.grid[x][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y:y+2] = [Wall(), Item()]
        world.grid[x+1][y+3] = Wall()
        world.grid[x+1][y+5:y+7] = [Item(), Wall()]
        
        world.grid[x+2][y] = Wall()
        world.grid[x+2][y+3] = Wall()
        world.grid[x+2][y+6] = Wall()
        
        world.grid[x+3][y] = Wall()
        world.grid[x+3][y+2:y+5] = [Item(), Wall(), Item()]
        world.grid[x+3][y+6] = Wall()
        
        world.grid[x+4][y:y+7] = [Wall(), Door(), Wall(), Wall(), Wall(), Door(), Wall()]
        
        world.grid[x+5][y] = Fence()
        world.grid[x+5][y+3] = Fence()
        world.grid[x+5][y+6] = Fence()
        
        world.grid[x+6][y] = Fence()
        world.grid[x+6][y+3] = Fence()
        world.grid[x+6][y+6] = Fence()
        
    # _ W W W W W W W
    # _ W i _ W _ i W
    # _ W _ _ W _ _ W
    # _ W _ i W i _ W
    # _ W D W W W D W
    # _ F _ _ F _ _ w
    # _ F _ _ F _ _ w
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house1B(world, x, y):
        Buildings.house1A(world, x, y+1)

    # _ _ _ _ _ _ _ _
    # F _ _ F _ _ F _
    # F _ _ F _ _ F _
    # W D W W W D W _
    # W _ i W i _ W _
    # W _ _ W _ _ W _
    # W i _ W _ i W _
    # W W W W W W W _
    @staticmethod
    def house1C(world, x, y):
        world.grid[x+1][y] = Fence()
        world.grid[x+1][y+3] = Fence()
        world.grid[x+1][y+6] = Fence()
        
        world.grid[x+2][y] = Fence()
        world.grid[x+2][y+3] = Fence()
        world.grid[x+2][y+6] = Fence()
        
        world.grid[x+3][y:y+7] = [Wall(), Door(), Wall(), Wall(), Wall(), Door(), Wall()]
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+2:y+5] = [Item(), Wall(), Item()]
        world.grid[x+4][y+6] = Wall()
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+3] = Wall()
        world.grid[x+5][y+6] = Wall()
        
        world.grid[x+6][y:y+2] = [Wall(), Item()]
        world.grid[x+6][y+3] = Wall()
        world.grid[x+6][y+5:y+7] = [Item(), Wall()]
        
        world.grid[x+7][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]

    # _ _ _ _ _ _ _ _
    # _ F _ _ F _ _ w
    # _ F _ _ F _ _ w
    # _ W D W W W D W
    # _ W _ i W i _ W
    # _ W _ _ W _ _ W
    # _ W i _ W _ i W
    # _ W W W W W W W
    @staticmethod
    def house1D(world, x, y):
        Buildings.house1C(world, x, y+1)
        
    # W W W W W W W _
    # W i _ W i i W _
    # W _ _ D _ _ W _
    # W _ _ W W W W _
    # W _ _ _ _ i W _
    # W W D W W W W _
    # _ _ _ _ _ _ _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house2A(world, x, y):
        world.grid[x][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y:y+2] = [Wall(), Item()]
        world.grid[x+1][y+3:y+7] = [Wall(), Item(), Item(), Wall()]
        
        world.grid[x+2][y] = Wall()
        world.grid[x+2][y+3] = Door()
        world.grid[x+2][y+6] = Wall()
        
        world.grid[x+3][y] = Wall()
        world.grid[x+3][y+3:y+7] = [Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+5:y+7] = [Item(), Wall()]
        
        world.grid[x+5][y:y+7] = [Wall(), Wall(), Door(), Wall(), Wall(), Wall(), Wall()]
        
    # _ W W W W W W W
    # _ W i _ W i i W
    # _ W _ _ D _ _ W
    # _ W _ _ W W W W
    # _ W _ _ _ _ i W
    # _ W W D W W W W
    # _ _ _ _ _ _ _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house2B(world, x, y):
        Buildings.house2A(world, x, y+1)
        
    # _ _ _ _ _ _ _ _
    # _ _ _ _ _ _ _ _
    # W W D W W W W _
    # W _ _ _ _ i W _
    # W _ _ W W W W _
    # W _ _ D _ _ W _
    # W i _ W i i W _
    # W W W W W W W _
    @staticmethod
    def house2C(world, x, y):
        world.grid[x+2][y:y+7] = [Wall(), Wall(), Door(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+3][y] = Wall()
        world.grid[x+3][y+5:y+7] = [Item(), Wall()]
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+3:y+7] = [Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+3] = Door()
        world.grid[x+5][y+6] = Wall()
        
        world.grid[x+6][y:y+2] = [Wall(), Item()]
        world.grid[x+6][y+3:y+7] = [Wall(), Item(), Item(), Wall()]
        
        world.grid[x+7][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
    
    # _ _ _ _ _ _ _ _
    # _ _ _ _ _ _ _ _
    # _ W W D W W W W
    # _ W _ _ _ _ i W
    # _ W _ _ W W W W
    # _ W _ _ D _ _ W
    # _ W i _ W i i W
    # _ W W W W W W W
    @staticmethod
    def house2D(world, x, y):
        Buildings.house2C(world, x, y+1)    
        
    # W W W W W W W _
    # W i _ _ i _ W _
    # W _ _ i _ _ W _
    # W _ _ _ _ i W _
    # W W W D W W W _
    # _ _ F _ F _ _ _
    # _ _ F _ F _ _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house3A(world, x, y):
        world.grid[x][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y:y+2] = [Wall(), Item()]
        world.grid[x+1][y+4] = Item()
        world.grid[x+1][y+6] = Wall()
        
        world.grid[x+2][y] = Wall()
        world.grid[x+2][y+3] = Item()
        world.grid[x+2][y+6] = Wall()
        
        world.grid[x+3][y] = Wall()
        world.grid[x+3][y+5:y+7] = [Item(), Wall()]
        
        world.grid[x+4][y:y+7] = [Wall(), Wall(), Wall(), Door(), Wall(), Wall(), Wall()]
        
        world.grid[x+5][y+2] = Fence()
        world.grid[x+5][y+4] = Fence()
        
        world.grid[x+6][y+2] = Fence()
        world.grid[x+6][y+4] = Fence()
    
    # _ W W W W W W W
    # _ W i _ _ i _ W
    # _ W _ _ i _ _ W
    # _ W _ _ _ _ i W
    # _ W W W D W W W
    # _ _ _ F _ F _ _
    # _ _ _ F _ F _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house3B(world, x, y):
        Buildings.house3A(world, x, y+1)    
        
    # _ _ _ _ _ _ _ _
    # _ _ F _ F _ _ _
    # _ _ F _ F _ _ _
    # W W W D W W W _
    # W _ _ _ _ i W _
    # W _ _ i _ _ W _
    # W i _ _ i _ W _
    # W W W W W W W _
    @staticmethod
    def house3C(world, x, y):
        world.grid[x+1][y+2] = Fence()
        world.grid[x+1][y+4] = Fence()
        
        world.grid[x+2][y+2] = Fence()
        world.grid[x+2][y+4] = Fence()
        
        world.grid[x+3][y:y+7] = [Wall(), Wall(), Wall(), Door(), Wall(), Wall(), Wall()]
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+5:y+7] = [Item(), Wall()]
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+3] = Item()
        world.grid[x+5][y+6] = Wall()
        
        world.grid[x+6][y:y+2] = [Wall(), Item()]
        world.grid[x+6][y+4] = Item()
        world.grid[x+6][y+6] = Wall()
        
        world.grid[x+7][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
    # _ _ _ _ _ _ _ _
    # _ _ _ F _ F _ _
    # _ _ _ F _ F _ _
    # _ W W W D W W W
    # _ W _ _ _ _ i W
    # _ W _ _ i _ _ W
    # _ W i _ _ i _ W
    # _ W W W W W W W
    @staticmethod
    def house3D(world, x, y):
        Buildings.house3C(world, x, y+1)
        

    