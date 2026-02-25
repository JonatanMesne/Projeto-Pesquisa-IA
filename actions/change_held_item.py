from actions.action import Action

class ChangeHeldItem(Action):     #class for the action of changing the item in the agent's hands
    def __init__(self):
        super().__init__(0) #action takes 0 time units

    @staticmethod
    def action(state) -> bool:
        if state.index >= 0 and state.index < len(state.agent.inventory):
            state.agent.item_in_hand = state.agent.inventory[state.index]
            return True
        return False