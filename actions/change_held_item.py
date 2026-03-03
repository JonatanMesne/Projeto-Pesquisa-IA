from actions.action import Action

class ChangeHeldItem(Action):     #class for the action of changing the item in the agent's hands
    duration = 0
    need_index = True

    @staticmethod
    def action(state) -> bool:
        if state.index == -1:  # If index is -1, the agent wants to empty their hands
            state.agent.item_in_hand = None
            print("You removed the item from your hands.")
            return True
        if state.index >= 0 and state.index < len(state.agent.inventory):
            state.agent.item_in_hand = state.agent.inventory[state.index]
            print(f"You are now holding: {state.agent.item_in_hand.__class__.__name__}")
            return True
        print("Invalid index. No item in hand.")
        return False