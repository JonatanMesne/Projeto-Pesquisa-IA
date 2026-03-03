class WorldObject:
    #construtor
    def __init__(self, appearence='-', is_solid = False, is_destructible = False, 
                 durability = -1, has_action = False, action = None):
        self.appearence = appearence
        self.is_solid = is_solid
        self.is_destructible = is_destructible
        self.durability = durability
        self.has_action = has_action
        self.action = action
    
    def __str__(self) -> str:
        return self.__class__.__name__