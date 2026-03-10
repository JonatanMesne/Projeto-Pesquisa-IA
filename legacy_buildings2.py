from world_objects.ground import Ground
from world_objects.door import Door
from world_objects.wall import Wall
from world_objects.fence import Fence

from items.ammo import Ammo
from items.medkit import Medkit
from items.weapons.baseball_bat import BaseballBat
from items.weapons.knife import Knife
from items.weapons.pistol import Pistol
from items.weapons.smg import Smg

class Buildings:
    # _ W W W W W W W
    # _ W _ _ W _ _ W
    # _ W _ _ W _ _ W
    # _ W _ _ W _ _ W
    # _ W D W W W D W
    # _ F _ _ F _ _ w
    # _ F _ _ F _ _ w
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house1A(world, variant, x, y):
        world.grid[x][y + 1:y + 8] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x + 1][y + 1] = Wall()
        world.grid[x + 1][y + 4] = Wall()
        world.grid[x + 1][y + 7] = Wall()
        
        world.grid[x + 2][y + 1] = Wall()
        world.grid[x + 2][y + 4] = Wall()
        world.grid[x + 2][y + 7] = Wall()
        
        world.grid[x + 3][y + 1] = Wall()
        world.grid[x + 3][y + 4] = Wall()
        world.grid[x + 3][y + 7] = Wall()
        
        world.grid[x + 4][y + 1:y + 8] = [Wall(), Door(), Wall(), Wall(), Wall(), Door(), Wall()]
        
        world.grid[x + 5][y + 1] = Fence()
        world.grid[x + 5][y + 4] = Fence()
        world.grid[x + 5][y + 7] = Fence()
        
        world.grid[x + 6][y + 1] = Fence()
        world.grid[x + 6][y + 4] = Fence()
        world.grid[x + 6][y + 7] = Fence()
        
    # W W W W W F w _
    # W _ _ _ D _ _ _
    # W _ _ _ W _ _ _
    # W W W W W F w _
    # W _ _ _ W _ _ _
    # W _ _ _ D _ _ _
    # W W W W W F w _
    # _ _ _ _ _ _ _ _   
    @staticmethod
    def house1B(world, variant, x, y):
        world.grid[x][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Fence(), Fence()]
        
        world.grid[x+1][y] = Wall()
        world.grid[x+1][y+4] = Door()
        
        world.grid[x+2][y] = Wall()
        world.grid[x+2][y+4] = Wall()
        
        world.grid[x+3][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Fence(), Fence()]
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+4] = Wall()
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+4] = Door()
        
        world.grid[x+6][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Fence(), Fence()]

    # _ _ _ _ _ _ _ _
    # _ F w W W W W W
    # _ _ _ D _ _ _ W
    # _ _ _ W _ _ _ W
    # _ F w W W W W W
    # _ _ _ W _ _ _ W
    # _ _ _ D _ _ _ W
    # _ F w W W W W W
    @staticmethod
    def house1C(world, variant, x, y):
        world.grid[x+1][y+1:y+8] = [Fence(), Fence(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+2][y+3] = Door()
        world.grid[x+2][y+7] = Wall()
        
        world.grid[x+3][y+3] = Wall()
        world.grid[x+3][y+7] = Wall()
        
        world.grid[x+4][y+1:y+8] = [Fence(), Fence(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+5][y+3] = Wall()
        world.grid[x+5][y+7] = Wall()
        
        world.grid[x+6][y+3] = Door()
        world.grid[x+6][y+7] = Wall()
        
        world.grid[x+7][y+1:y+8] = [Fence(), Fence(), Wall(), Wall(), Wall(), Wall(), Wall()]

    # _ _ _ _ _ _ _ _
    # F _ _ F _ _ F _
    # F _ _ F _ _ F _
    # W D W W W D W _
    # W _ _ W _ _ W _
    # W _ _ W _ _ W _
    # W _ _ W _ _ W _
    # W W W W W W W _
    @staticmethod
    def house1D(world, variant, x, y):
        world.grid[x+1][y] = Fence()
        world.grid[x+1][y+3] = Fence()
        world.grid[x+1][y+6] = Fence()
        
        world.grid[x+2][y] = Fence()
        world.grid[x+2][y+3] = Fence()
        world.grid[x+2][y+6] = Fence()
        
        world.grid[x+3][y:y+7] = [Wall(), Door(), Wall(), Wall(), Wall(), Door(), Wall()]
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+3] = Wall()
        world.grid[x+4][y+6] = Wall()
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+3] = Wall()
        world.grid[x+5][y+6] = Wall()
        
        world.grid[x+6][y] = Wall()
        world.grid[x+6][y+3] = Wall()
        world.grid[x+6][y+6] = Wall()
        
        world.grid[x+7][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
    # _ W W W W W W W
    # _ W _ _ W _ _ W
    # _ W _ _ D _ _ W
    # _ W _ _ W W W W
    # _ W _ _ _ _ _ W
    # _ W W D W W W W
    # _ _ _ _ _ _ _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house2A(world, variant, x, y):
        world.grid[x][y+1:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y+1] = Wall()
        world.grid[x+1][y+4] = Wall()
        world.grid[x+1][y+7] = Wall()
        
        world.grid[x+2][y+1] = Wall()
        world.grid[x+2][y+4] = Door()
        world.grid[x+2][y+7] = Wall()
        
        world.grid[x+3][y+1] = Wall()
        world.grid[x+3][y+4:y+8] = [Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+4][y+1] = Wall()
        world.grid[x+4][y+7] = Wall()
        
        world.grid[x+5][y+1:y+8] = [Wall(), Wall(), Door(), Wall(), Wall(), Wall(), Wall()]
        
    # W W W W W W _ _
    # W _ _ _ _ W _ _
    # W _ _ _ _ D _ _
    # W W D W _ W _ _
    # W _ _ W _ W _ _
    # W _ _ W _ W _ _
    # W W W W W W _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house2B(world, variant, x, y):
        world.grid[x][y:y+6] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y] = Wall()
        world.grid[x+1][y+5] = Wall()
        
        world.grid[x+2][y] = Wall()
        world.grid[x+2][y+5] = Door()
        
        world.grid[x+3][y:y+4] = [Wall(), Wall(), Door(), Wall()]
        world.grid[x+3][y+5] = Wall()
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+3] = Wall()
        world.grid[x+4][y+5] = Wall()
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+3] = Wall()
        world.grid[x+5][y+5] = Wall()
        
        world.grid[x+6][y:y+6] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
    # _ _ _ _ _ _ _ _
    # _ _ W W W W W W
    # _ _ W _ _ _ _ W
    # _ _ D _ _ _ _ W
    # _ _ W _ W D W W
    # _ _ W _ W _ _ W
    # _ _ W _ W _ _ W
    # _ _ W W W W W W
    @staticmethod
    def house2C(world, variant, x, y):
        world.grid[x+1][y+2:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+2][y+2] = Wall()
        world.grid[x+2][y+7] = Wall()
        
        world.grid[x+3][y+2] = Door()
        world.grid[x+3][y+7] = Wall()
        
        world.grid[x+4][y+2] = Wall()
        world.grid[x+4][y+4:y+8] = [Wall(), Door(), Wall(), Wall()]
        
        world.grid[x+5][y+2] = Wall()
        world.grid[x+5][y+4] = Wall()
        world.grid[x+5][y+7] = Wall()
        
        world.grid[x+6][y+2] = Wall()
        world.grid[x+6][y+4] = Wall()
        world.grid[x+6][y+7] = Wall()
        
        world.grid[x+7][y+2:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]

    # _ _ _ _ _ _ _ _
    # _ _ _ _ _ _ _ _
    # W W D W W W W _
    # W _ _ _ _ _ W _
    # W _ _ W W W W _
    # W _ _ D _ _ W _
    # W _ _ W _ _ W _
    # W W W W W W W _
    @staticmethod
    def house2D(world, variant, x, y):
        world.grid[x+2][y:y+7] = [Wall(), Wall(), Door(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+3][y] = Wall()
        world.grid[x+3][y+6] = Wall()
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+3:y+7] = [Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+3] = Door()
        world.grid[x+5][y+6] = Wall()
        
        world.grid[x+6][y] = Wall()
        world.grid[x+6][y+3] = Wall()
        world.grid[x+6][y+6] = Wall()
        
        world.grid[x+7][y:y+7] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
    # _ W W W W W W W
    # _ W _ _ _ _ _ W
    # _ W _ _ _ _ _ W
    # _ W _ _ _ _ _ W
    # _ W W W D W W W
    # _ _ _ F _ F _ _
    # _ _ _ F _ F _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house3A(world, variant, x, y):
        world.grid[x][y+1:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y+1] = Wall()
        world.grid[x+1][y+7] = Wall()
        
        world.grid[x+2][y+1] = Wall()
        world.grid[x+2][y+7] = Wall()
        
        world.grid[x+3][y+1] = Wall()
        world.grid[x+3][y+7] = Wall()
        
        world.grid[x+4][y+1:y+8] = [Wall(), Wall(), Wall(), Door(), Wall(), Wall(), Wall()]
        
        world.grid[x+5][y+3] = Fence()
        world.grid[x+5][y+5] = Fence()
        
        world.grid[x+6][y+3] = Fence()
        world.grid[x+6][y+5] = Fence()

    # W W W W W _ _ _
    # W _ _ _ W _ _ _
    # W _ _ _ W F w _
    # W _ _ _ D _ _ _
    # W _ _ _ W F w _
    # W _ _ _ W _ _ _
    # W W W W W _ _ _
    # _ _ _ _ _ _ _ _
    @staticmethod
    def house3B(world, variant, x, y):
        world.grid[x][y:y+5] = [Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+1][y] = Wall()
        world.grid[x+1][y+4] = Wall()
        
        world.grid[x+2][y] = Wall()
        world.grid[x+2][y+4:y+7] = [Wall(), Fence(), Fence()]
        
        world.grid[x+3][y] = Wall()
        world.grid[x+3][y+4] = Door()
        
        world.grid[x+4][y] = Wall()
        world.grid[x+4][y+4:y+7] = [Wall(), Fence(), Fence()]
        
        world.grid[x+5][y] = Wall()
        world.grid[x+5][y+4] = Wall()
        
        world.grid[x+6][y:y+5] = [Wall(), Wall(), Wall(), Wall(), Wall()]
        
    # _ _ _ _ _ _ _ _
    # _ _ _ W W W W W
    # _ _ _ W _ _ _ W
    # _ F w W _ _ _ W
    # _ _ _ D _ _ _ W
    # _ F w W _ _ _ W
    # _ _ _ W _ _ _ W
    # _ _ _ W W W W W
    @staticmethod
    def house3C(world, variant, x, y):
        world.grid[x+1][y+3:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall()]
        
        world.grid[x+2][y+3] = Wall()
        world.grid[x+2][y+7] = Wall()
        
        world.grid[x+3][y+1:y+3] = [Fence(), Fence()]
        world.grid[x+3][y+3] = Wall()
        world.grid[x+3][y+7] = Wall()
        
        world.grid[x+4][y+3] = Door()
        world.grid[x+4][y+7] = Wall()
        
        world.grid[x+5][y+1:y+3] = [Fence(), Fence()]
        world.grid[x+5][y+3] = Wall()
        world.grid[x+5][y+7] = Wall()
        
        world.grid[x+6][y+3] = Wall()
        world.grid[x+6][y+7] = Wall()
        
        world.grid[x+7][y+3:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall()]

    # _ _ _ _ _ _ _ _
    # _ _ F _ F _ _ _
    # _ _ F _ F _ _ _
    # W W W D W W W _
    # W _ _ _ _ _ W _
    # W _ _ _ _ _ W _
    # W _ _ _ _ _ W _
    # W W W W W W W _
    @staticmethod
    def house3D(world, variant, x, y):
        world.grid[x][y+3] = Fence()
        world.grid[x][y+5] = Fence()
        
        world.grid[x+1][y+3] = Fence()
        world.grid[x+1][y+5] = Fence()
        
        world.grid[x+2][y+1:y+8] = [Wall(), Wall(), Wall(), Door(), Wall(), Wall(), Wall()]
        
        world.grid[x+3][y+1] = Wall()
        world.grid[x+3][y+7] = Wall()
        
        world.grid[x+4][y+1] = Wall()
        world.grid[x+4][y+7] = Wall()
        
        world.grid[x+5][y+1] = Wall()
        world.grid[x+5][y+7] = Wall()
        
        world.grid[x+6][y+1:y+8] = [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]