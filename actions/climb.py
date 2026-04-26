from actions.action import Action
from actions.walk import Walk
from world_objects.world_object import WorldObject

class Climb(Action):     #class for the action of climbing a small wall
    duration = 2
    need_direction = True
    id = 13 #to 16

    @staticmethod
    def action(state) -> int:
        if state.agent.stamina > 10 and state.agent.status[3] == 0:
            direction = state.current_action_id - Climb.id  # Calculate direction based on action ID
            world_object = state.get_world_object_in_front(direction)
            if isinstance(world_object, WorldObject) and world_object.action.__class__.__name__ == 'Climb':
                world_object.is_solid = False
                state.current_action_id = direction + 1  # Adjust the action ID to correspond to walking in the same direction
                Walk.action(state)
                world_object.is_solid = True
                state.agent.stamina -= 10
                print("You climbed over the obstacle.")
                return 5
        print("Climb failed: not enough stamina or no climbable object in front.")
        return -100