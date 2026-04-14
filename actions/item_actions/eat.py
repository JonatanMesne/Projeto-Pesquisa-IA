from actions.action import Action

class Eat(Action):     #class for the action of eating food
    duration = 1

    @staticmethod
    def action(state) -> bool:
        if(state.agent.item_in_hand.__class__.__name__ == "Food"):
            food = state.agent.item_in_hand
            state.agent.hunger = max(0, state.agent.hunger - food.hunger_satiation)
            state.agent.inventory.remove(food)
            state.agent.inventory_space_used -= food.inventory_space
            state.agent.item_in_hand = None
            if "hungry" in state.agent.status:
                state.agent.status.remove("hungry")
            print(f"You ate food and reduced your hunger by {food.hunger_satiation}. Current hunger: {state.agent.hunger}")
            return True
        else:
            print("You need to have food in hand to eat.")
            return False