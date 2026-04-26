from actions.action import Action

class Eat(Action):     #class for the action of eating food
    duration = 1
    id = 22

    @staticmethod
    def action(state) -> int:
        if(state.agent.item_in_hand.__class__.__name__ == "Food"):
            food = state.agent.item_in_hand
            state.agent.hunger = max(0, state.agent.hunger - food.hunger_satiation)
            state.agent.inventory.remove(food)
            state.agent.inventory_space_used -= food.inventory_space
            state.agent.item_in_hand = None
            state.agent.status[1] = 0
            print(f"You ate food and reduced your hunger by {food.hunger_satiation}. Current hunger: {state.agent.hunger}")
            return food.hunger_satiation / 2
        else:
            print("You need to have food in hand to eat.")
            return -100