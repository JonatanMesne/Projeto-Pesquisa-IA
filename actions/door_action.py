from actions.action import Action

class DoorAction(Action):   #class for opening and closing doors
    def __init__(self):
        super().__init__(1) #action takes 1 time unit
        
    @staticmethod
    def action(state) -> bool:
        state.advance_time()
        world_object = state.get_world_object_in_front()
        if(isinstance(world_object.action, DoorAction)):
            #Toggle door state between open and closed
            if(world_object.is_solid == True):
                world_object.appearence = 'd'  #Open door
                world_object.is_solid = False
            else:
                world_object.appearence = 'D'  #Closed door
                world_object.is_solid = True
            return True
        else:
            return False