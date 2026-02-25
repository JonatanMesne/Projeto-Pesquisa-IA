from actions.action import Action
from actions.walk import Walk

class Climb(Action):     #class for the action of climbing a small wall
    def __init__(self):
        super().__init__(2) #action takes 2 time unit

    @staticmethod
    def action(state) -> bool:
        world_object = state.get_world_object_in_front()
        if(isinstance(world_object.action, Climb)):
            #first timestep: standby
            state.advance_time()
            #second timestep: move to the top of the small wall
            state.advance_time()
            world_object.is_solid = False
            Walk.action(state)
            world_object.is_solid = True
            return True
        else:
            return False