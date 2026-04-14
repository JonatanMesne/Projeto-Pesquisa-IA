from actions.action import Action

class Drink(Action):     #class for the action of drinking water
    duration = 1

    @staticmethod
    def action(state) -> bool:
        if(state.agent.item_in_hand.__class__.__name__ == "Water"):
            water = state.agent.item_in_hand
            state.agent.thirst = max(0, state.agent.thirst - water.thirst_satiation)
            state.agent.inventory.remove(water)
            state.agent.inventory_space_used -= water.inventory_space
            state.agent.item_in_hand = None
            if "thirsty" in state.agent.status:
                state.agent.status.remove("thirsty")
            print(f"You drank water and reduced your thirst by {water.thirst_satiation}. Current thirst: {state.agent.thirst}")
            return True
        else:
            print("You need to have water in hand to drink.")
            return False