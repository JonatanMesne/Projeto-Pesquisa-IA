from actions.action import Action
from actions.walk import Walk

class Climb(Action):     #class for the action of climbing a small wall
    duration = 2
    need_direction = True

    @staticmethod
    def action(state) -> bool:
        if state.agent.stamina > 10 and "tired" not in state.agent.status:
            world_object = state.get_world_object_in_front()
            if world_object.action.__name__ == 'Climb':
                world_object.is_solid = False
                Walk.action(state)
                world_object.is_solid = True
                state.agent.stamina -= 10
                print("You climbed over the obstacle.")
                return True
        print("Climb failed: not enough stamina or no climbable object in front.")
        return False