from world_objects.world_object import WorldObject

class Ground(WorldObject):
    def __init__(self):
        super().__init__(appearence='_', is_solid=False, is_destructible=False, durability=1000, has_action=False, action=None)
    