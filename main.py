from items.item import Item
from items.ammo import Ammo
from items.medkit import Medkit
from items.food import Food
from items.water import Water
from items.weapons.baseball_bat import BaseballBat
from items.weapons.knife import Knife
from items.weapons.pistol import Pistol
from items.weapons.smg import Smg

from state import State

#direction = 1 (up) | 2 (right) | 3 (down) | 4 (left)
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

estado = State()

while True:
    estado.reset(seed='', player_controlled=True, time_limit=1000)

    # print(estado.world)

    # estado.agent.inventory = [Ammo(), Medkit(), Food(), Water(), BaseballBat(), Knife(), Pistol(), Smg()]

    estado.environment_start()