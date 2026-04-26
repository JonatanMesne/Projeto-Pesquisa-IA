from actions.action import Action
from actions.walk import Walk

class Climb(Action):     #class for the action of climbing a small wall
    duration = 2
    need_direction = True
    id = 13 #to 16

    @staticmethod
    def action(state) -> bool:
        if state.agent.stamina > 10 and "tired" not in state.agent.status:
            direction = state.current_action_id - Climb.id  # Calculate direction based on action ID
            world_object = state.get_world_object_in_front(direction)
            if world_object.action.__name__ == 'Climb':
                world_object.is_solid = False
                state.current_action_id = direction + 1  # Adjust the action ID to correspond to walking in the same direction
                Walk.action(state)
                world_object.is_solid = True
                state.agent.stamina -= 10
                print("You climbed over the obstacle.")
                return True
        print("Climb failed: not enough stamina or no climbable object in front.")
        return False