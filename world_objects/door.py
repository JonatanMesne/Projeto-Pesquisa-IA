from world_objects.world_object import WorldObject
from actions.door_action import DoorAction

class Door(WorldObject):
    def __init__(self):
        super().__init__(appearence='D', is_solid=True, is_destructible=True, durability=5, has_action=True, action=DoorAction)  #ação = abrir/fechar