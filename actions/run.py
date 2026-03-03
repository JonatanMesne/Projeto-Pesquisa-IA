from actions.action import Action
from actions.walk import Walk

class Run(Action):     #class for the action of running a few tiles
    duration = 1
    need_direction = True
    
    run_distance = 3

    @staticmethod
    def action(state) -> bool:
        return_value = False
        if "tired" not in state.agent.status:
            for i in range(Run.run_distance):
                if state.agent.stamina >= 5:
                    state.agent.stamina -= 5
                    if Walk.action(state):
                        return_value = True
                    else:
                        if return_value:
                            print(f"You ran {i} tiles before being stopped.")
                        break
                else:
                    if return_value:
                        print(f"You ran {i} tiles before being stopped.")
                    break
        if return_value:
            print(f"You ran 3 tiles before being stopped.")
        else:
            print("You are too tired to run or hit a solid object.")
        return return_value