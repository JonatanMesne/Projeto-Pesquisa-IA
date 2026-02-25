from items.item import Item
from abc import ABC

class RangedWeapon(Item, ABC):
    def __init__(self, appearence='r', action=[], inventory_space=2, range=3, damage=5, pierce=1, ammo_capacity=5, fire_rate=1):
        super().__init__(appearence=appearence, action=action, inventory_space=inventory_space)
        self.damage = damage
        self.range = range
        self.pierce = pierce
        self.ammo_capacity = ammo_capacity
        self.ammo = self.ammo_capacity
        self.fire_rate = fire_rate #projectiles per time step
        
    def print_status(self):
        print(f'Ammo: {self.ammo}/{self.ammo_capacity}')