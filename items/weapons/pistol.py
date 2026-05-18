from items.weapons.ranged import RangedWeapon

class Pistol(RangedWeapon):
    id = 31
    def __init__(self):
        super().__init__(appearence='p', range=6, damage=8, pierce=2, 
                         ammo_capacity=15, fire_rate=1)