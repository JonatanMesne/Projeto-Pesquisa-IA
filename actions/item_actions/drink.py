from actions.action import Action

class Drink(Action):     #class for the action of drinking water
    duration = 1
    id = 21

    @staticmethod
    def action(state) -> int:
        if(state.agent.item_in_hand.__class__.__name__ == "Water"):
            water = state.agent.item_in_hand
            state.agent.thirst = max(0, state.agent.thirst - water.thirst_satiation)
            state.agent.inventory.remove(water)
            state.agent.inventory_space_used -= water.inventory_space
            state.agent.item_in_hand = None
            state.agent.status[0] = 0
            if(state.prints_enabled):
                print(f"You drank water and reduced your thirst by {water.thirst_satiation}. Current thirst: {state.agent.thirst}")
            return water.thirst_satiation
        else:
            if(state.prints_enabled):
                print("You need to have water in hand to drink.")
            return state.invalid_return_value