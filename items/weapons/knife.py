from items.weapons.melee import MeleeWeapon

class Knife(MeleeWeapon):
    id = 41
    def __init__(self):
        super().__init__(appearence='k', range=2, damage=10, knockback=1)