from items.item import Item
from abc import ABC

class MeleeWeapon(Item, ABC):
    def __init__(self, appearence='m', action=[], inventory_space=2, range=1, damage=5, knockback=0):
        super().__init__(appearence=appearence, action=action, inventory_space=inventory_space)
        self.damage = damage
        self.range = range
        self.knockback = knockback #tiles pushed back on hit, can be negative for pull weapons