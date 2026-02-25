from entities.zombie import Zombie
from items.ammo import Ammo
from items.medkit import Medkit
from items.weapons.baseball_bat import BaseballBat
from items.weapons.knife import Knife
from items.weapons.pistol import Pistol
from items.weapons.smg import Smg
from world import World
from entities.agent import Agent
from state import State
from world_objects.door import Door
from actions.walk import Walk
from actions.door_action import DoorAction
from actions.climb import Climb
from actions.pickup_item import PickupItem
from actions.update_vision import UpdateVision
from items.weapons.ranged import RangedWeapon
from actions.item_actions.attack import Attack

mapa = World()

#direction = 1 (up) | 2 (right) | 3 (down) | 4 (left)
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

estado = State()

agente = Agent()

mapa.generateMap(agente)

# print(mapa)

mapa.generateBuildings() 

print(mapa)

estado.agent = agente
estado.map_grid = mapa.grid

agente.update_possible_actions(estado)

agente.print_actions()