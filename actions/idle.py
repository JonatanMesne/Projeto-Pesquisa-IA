from actions.action import Action

class Idle(Action):     #class for the action of doing nothing for 1 time unit
    duration = 1
    id = 0

    @staticmethod
    def action(state) -> int:
        state.agent.stamina = min(state.agent.stamina + 20, state.agent.max_stamina)
        print("You take a moment to rest and recover stamina.")
        return 5