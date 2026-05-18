from actions.action import Action
from items.food import Food

class Eat(Action):     #class for the action of eating food
    duration = 1
    id = 18

    @staticmethod
    def action(state) -> int:
        if(state.agent.inventory_qtt[2] > 0):   # Check if there is food in inventory
            food = state.agent.find_item_in_inventory(Food.id)  # Find the food item in inventory
            state.agent.hunger = max(0, state.agent.hunger - food.hunger_satiation)
            state.agent.inventory.remove(food)
            state.agent.inventory_qtt[2] -= 1
            state.agent.status[1] = 0
            if(state.prints_enabled):
                print(f"You ate food and reduced your hunger by {food.hunger_satiation}. Current hunger: {state.agent.hunger}")
            if (state.agent.hunger == state.agent.max_hunger and 
                state.agent.inventory_qtt[2] != state.agent.max_inventory_qtt[2] - 1):
                return -10
            return food.hunger_satiation * 2
        else:
            if(state.prints_enabled):
                print("You need to have food in the inventory to eat.")
            return state.invalid_return_value