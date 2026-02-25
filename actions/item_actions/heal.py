from actions.action import Action

class Heal(Action):     #class for the action of perceiving the surroundings
    def __init__(self):
        super().__init__(1) #action takes 1 time units

    @staticmethod
    def action(state) -> bool:
        state.agent.health += state.agent.item_in_hand.heal_amount
        if state.agent.health > state.agent.max_health:
            state.agent.health = state.agent.max_health
        state.agent.remove_item(state.agent.item_in_hand)
        state.agent.item_in_hand = None
        state.advance_time()
        return True