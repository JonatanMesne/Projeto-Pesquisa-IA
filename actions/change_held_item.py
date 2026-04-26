from actions.action import Action

class ChangeHeldItem(Action):     #class for the action of changing the item in the agent's hands
    duration = 0
    need_index = True
    id = 100 #to 100 + agent_inventory

    @staticmethod
    def action(state) -> bool:
        index = state.current_action_id - ChangeHeldItem.id  # Calculate index based on action ID
        if index == 0:  # If index is 0, the agent wants to empty their hands
            state.agent.item_in_hand = None
            print("You removed the item from your hands.")
            return True
        if index >= 1 and index < len(state.agent.inventory) + 1:
            state.agent.item_in_hand = state.agent.inventory[index-1]  # Set the item in hand to the selected inventory item
            print(f"You are now holding: {state.agent.item_in_hand.__class__.__name__}")
            return True
        print("Invalid index. No item in hand.")
        return False