from actions.action import Action

class Idle(Action):     #class for the action of doing nothing for 1 time unit
    duration = 1
    id = 0
    stamina_recovery = 20

    @staticmethod
    def action(state) -> int:
        state.agent.stamina = min(state.agent.stamina + Idle.stamina_recovery, state.agent.max_stamina)
        if(state.prints_enabled):
            print("You take a moment to rest and recover stamina.")
        if state.agent.stamina == state.agent.max_stamina:
            return -500
        return 5