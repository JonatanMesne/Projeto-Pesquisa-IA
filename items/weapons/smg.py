from items.weapons.ranged import RangedWeapon

class Smg(RangedWeapon):
    id = 32
    def __init__(self):
        super().__init__(appearence='s', action=[], inventory_space=3, 
                         range=4, damage=7, pierce=1, ammo_capacity=30, fire_rate=3)