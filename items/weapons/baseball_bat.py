from items.weapons.melee import MeleeWeapon

class BaseballBat(MeleeWeapon):
    def __init__(self):
        super().__init__(appearence='b', action=[], inventory_space=2, 
                         range=3, damage=8, knockback=2)