from actions.action import Action
from items.water import Water

class Drink(Action):     #class for the action of drinking water
    duration = 1
    id = 17

    @staticmethod
    def action(state) -> int:
        if(state.agent.inventory_qtt[3] > 0):  # Check if there is water in inventory
            water = state.agent.find_item_in_inventory(Water.id)  # type: ignore
            state.agent.thirst = max(0, state.agent.thirst - water.thirst_satiation)
            state.agent.inventory.remove(water)
            state.agent.inventory_qtt[3] -= 1
            state.agent.status[0] = 0
            if(state.prints_enabled):
                print(f"You drank water and reduced your thirst by {water.thirst_satiation}. Current thirst: {state.agent.thirst}")
            if (state.agent.thirst == state.agent.max_thirst and 
                state.agent.inventory_qtt[3] != state.agent.max_inventory_qtt[3] - 1):
                return -10
            return water.thirst_satiation * 2
        else:
            if(state.prints_enabled):
                print("You need to have water in the inventory to drink.")
            return state.invalid_return_value