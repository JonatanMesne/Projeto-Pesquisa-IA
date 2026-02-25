from world_objects.world_object import WorldObject

class Wall(WorldObject):
    def __init__(self):
        super().__init__(appearence='W', is_solid=True, is_destructible=True, durability=20, has_action=False, action=None)