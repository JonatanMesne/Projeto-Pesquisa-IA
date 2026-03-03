from world_objects.world_object import WorldObject
from actions.climb import Climb

class SmallWall(WorldObject):
    def __init__(self):
        super().__init__(appearence='w', is_solid=True, is_destructible=True, durability=6, has_action=True, action=Climb) #ação = escalar