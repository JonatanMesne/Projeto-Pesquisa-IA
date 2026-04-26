from actions.action import Action

class Heal(Action):     #class for the action of perceiving the surroundings
    duration = 1
    id = 23

    @staticmethod
    def action(state) -> int:
        if(state.agent.item_in_hand.__class__.__name__ == "Medkit"):
            state.agent.health += state.agent.item_in_hand.heal_amount
            if state.agent.health > state.agent.max_health:
                state.agent.health = state.agent.max_health
            state.agent.remove_item(state.agent.item_in_hand)
            state.agent.item_in_hand = None
            state.agent.status[2] = 0
            print(f"You used a medkit and healed {state.agent.item_in_hand.heal_amount} health. Current health: {state.agent.health}") # type: ignore
            return state.agent.item_in_hand.heal_amount / 2 # type: ignore
        else:
            print("You need to have a medkit in hand to heal.")
            return -100