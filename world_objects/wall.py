from world_objects.world_object import WorldObject

class Wall(WorldObject):
    id = 12
    def __init__(self):
        super().__init__(appearence='W', is_solid=True, is_destructible=True, durability=10, has_action=False, action=None)