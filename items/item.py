from world_objects.world_object import WorldObject
from abc import ABC

class Item(WorldObject, ABC):
    def __init__(self, appearence='i', action=[], inventory_space = 1):
        super().__init__(appearence, is_solid=False, is_destructible=False, durability=1000, has_action=True, action=action)
        self.inventory_space = inventory_space