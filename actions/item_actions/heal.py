from actions.action import Action

class Heal(Action):     #class for the action of perceiving the surroundings
    duration = 1
    id = 23

    @staticmethod
    def action(state) -> int:
        heal_item = state.agent.item_in_hand
        if(heal_item.__class__.__name__ == "Medkit"):
            state.agent.health += heal_item.heal_amount
            if state.agent.health > state.agent.max_health:
                state.agent.health = state.agent.max_health
            state.agent.inventory.remove(heal_item)
            state.agent.inventory_space_used -= heal_item.inventory_space
            state.agent.item_in_hand = None
            state.agent.status[2] = 0
            if(state.prints_enabled):
                print(f"You used a medkit and healed {heal_item.heal_amount} health. Current health: {state.agent.health}") # type: ignore
            return heal_item.heal_amount    # type: ignore
        else:
            if(state.prints_enabled):
                print("You need to have a medkit in hand to heal.")
            return state.invalid_return_value