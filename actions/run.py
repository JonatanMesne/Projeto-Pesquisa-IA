from actions.action import Action
from actions.walk import Walk

class Run(Action):     #class for the action of running a few tiles
    duration = 1
    need_direction = True
    id = 5  #to 8
    
    run_distance = 3

    @staticmethod
    def action(state) -> int:
        return_value = 0
        if state.agent.status[3] == 0:
            state.current_action_id = state.current_action_id - 4  # Adjust the action ID to correspond to walking in the same direction
            for _ in range(Run.run_distance):
                if state.agent.stamina >= 5:
                    if Walk.action(state) == 5:
                        state.agent.stamina -= 5
                        return_value += 3
                    else:
                        break
                else:
                    break
        if return_value > 0:
            if return_value // 3 < Run.run_distance:
                if(state.prints_enabled):
                    print(f"You ran {return_value // 3} tile{'s' if return_value > 1 else ''} before getting too tired or hitting a solid object.")
            else:
                if(state.prints_enabled):
                    print(f"You ran {Run.run_distance} tiles.")
            return return_value
        else:
            if(state.prints_enabled):
                print("You are too tired to run or hit a solid object.")
            return state.invalid_return_value