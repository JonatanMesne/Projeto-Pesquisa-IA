from items.weapons.melee import MeleeWeapon
from actions.attack import Attack

class Knife(MeleeWeapon):
    def __init__(self):
        super().__init__(appearence='k', action=[], inventory_space=1, 
                         range=2, damage=10, knockback=1)