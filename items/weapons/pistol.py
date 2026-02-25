from actions.item_actions.attack import Attack
from actions.item_actions.reload import Reload
from items.weapons.ranged import RangedWeapon

class Pistol(RangedWeapon):
    def __init__(self):
        super().__init__(appearence='p', action=[Attack.action, Reload.action], inventory_space=2, 
                         range=6, damage=8, pierce=2, ammo_capacity=15, fire_rate=1)