from items.weapons.melee import MeleeWeapon

class BaseballBat(MeleeWeapon):
    id = 42
    def __init__(self):
        super().__init__(appearence='b', range=3, damage=8, knockback=2)