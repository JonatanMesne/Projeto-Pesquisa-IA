from actions.action import Action

class Idle(Action):     #class for the action of doing nothing for 1 time unit
    duration = 1
    id = 0

    @staticmethod
    def action(state) -> int:
        if state.agent.stamina == state.agent.max_stamina:
            if(state.prints_enabled):
                print("You are already fully rested.")
            return state.invalid_return_value
        state.agent.stamina = min(state.agent.stamina + 20, state.agent.max_stamina)
        if(state.prints_enabled):
            print("You take a moment to rest and recover stamina.")
        return 5