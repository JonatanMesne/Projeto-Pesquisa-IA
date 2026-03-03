from actions.item_actions.unload import Unload
from actions.item_actions.reload import Reload
from items.weapons.ranged import RangedWeapon

class Pistol(RangedWeapon):
    def __init__(self):
        super().__init__(appearence='p', action=[Reload, Unload], inventory_space=2, 
                         range=6, damage=8, pierce=2, ammo_capacity=15, fire_rate=1)