from items.item import Item
from abc import ABC

class MeleeWeapon(Item, ABC):
    id = 40
    def __init__(self, appearence='m', action=[], inventory_space=2, range=1, damage=5, knockback=0):
        super().__init__(appearence=appearence, action=action, inventory_space=inventory_space)
        self.damage = damage
        self.range = range
        self.knockback = knockback #tiles pushed back on hit, can be negative for pull weapons
    
    def item_info(self) -> str:
        return f"{self.__class__.__name__}: Damage {self.damage} | Knockback {self.knockback} | Inventory Space: {self.inventory_space}"
        
    def detailed_item_info(self) -> str:
        return f"{self.__class__.__name__}: Damage {self.damage} | Range {self.range} | Knockback {self.knockback} | Inventory Space: {self.inventory_space}"