from actions.action import Action

class Heal(Action):     #class for the action of perceiving the surroundings
    duration = 1
    id = 23

    @staticmethod
    def action(state) -> bool:
        if(state.agent.item_in_hand.__class__.__name__ == "Medkit"):
            state.agent.health += state.agent.item_in_hand.heal_amount
            if state.agent.health > state.agent.max_health:
                state.agent.health = state.agent.max_health
            state.agent.remove_item(state.agent.item_in_hand)
            state.agent.item_in_hand = None
            if "bleeding" in state.agent.status:
                state.agent.status.remove("bleeding")
            print(f"You used a medkit and healed {state.agent.item_in_hand.heal_amount} health. Current health: {state.agent.health}") # type: ignore
            return True
        else:
            print("You need to have a medkit in hand to heal.")
            return False