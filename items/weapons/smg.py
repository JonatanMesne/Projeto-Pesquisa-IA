from items.weapons.ranged import RangedWeapon
from actions.item_actions.reload import Reload
from actions.item_actions.attack import Attack

class Smg(RangedWeapon):
    def __init__(self):
        super().__init__(appearence='s', action=[Attack.action, Reload.action], inventory_space=3, 
                         range=4, damage=7, pierce=1, ammo_capacity=30, fire_rate=3)