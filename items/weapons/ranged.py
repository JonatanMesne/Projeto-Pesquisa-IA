from items.item import Item
from actions.item_actions.reload import Reload
from actions.item_actions.unload import Unload
from abc import ABC

class RangedWeapon(Item, ABC):
    id = 30
    def __init__(self, appearence='r', action=[], inventory_space=2, range=3, damage=5, pierce=1, ammo_capacity=5, fire_rate=1):
        action.append(Reload)
        action.append(Unload)
        super().__init__(appearence=appearence, action=action, inventory_space=inventory_space)
        self.damage = damage
        self.range = range
        self.pierce = pierce
        self.ammo_capacity = ammo_capacity
        self.ammo = self.ammo_capacity
        self.fire_rate = fire_rate #projectiles per time step
        
    def item_info(self):
        return f"{self.__class__.__name__}: Damage {self.damage}x{self.fire_rate} | Range {self.range} | Ammo {self.ammo}/{self.ammo_capacity} | Inventory Space: {self.inventory_space}"
        
    def detailed_item_info(self) -> str:
        return f"{self.__class__.__name__}: Damage {self.damage}x{self.fire_rate} | Range {self.range} | Pierce {self.pierce} | Ammo {self.ammo}/{self.ammo_capacity} | Inventory Space: {self.inventory_space}"