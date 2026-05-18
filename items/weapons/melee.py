from items.item import Item
from abc import ABC

class MeleeWeapon(Item, ABC):
    id = 40
    def __init__(self, appearence='m', range=1, damage=5, knockback=0):
        super().__init__(appearence=appearence)
        self.damage = damage
        self.range = range
        self.knockback = knockback #tiles pushed back on hit, can be negative for pull weapons
    
    def item_info(self) -> str:
        return f"{self.__class__.__name__}: Damage {self.damage} | Knockback {self.knockback}"
        
    def detailed_item_info(self) -> str:
        return f"{self.__class__.__name__}: Damage {self.damage} | Range {self.range} | Knockback {self.knockback}"