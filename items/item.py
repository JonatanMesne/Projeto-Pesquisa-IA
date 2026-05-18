from world_objects.world_object import WorldObject
from abc import abstractmethod

class Item(WorldObject):
    id = 20
    def __init__(self, appearence='i'):
        super().__init__(appearence, is_solid=False, is_destructible=False, durability=1000, has_action=False, action=[])
        
    @abstractmethod
    def item_info(self) -> str:
        pass