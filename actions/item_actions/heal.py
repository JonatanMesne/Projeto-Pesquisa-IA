from actions.action import Action
from items.medkit import Medkit

class Heal(Action):     #class for the action of perceiving the surroundings
    duration = 1
    id = 19

    @staticmethod
    def action(state) -> int:
        if(state.agent.inventory_qtt[1] > 0):
            health_healed = state.agent.health
            heal_item = state.agent.find_item_in_inventory(Medkit.id)
            state.agent.health = min(state.agent.max_health, state.agent.health + heal_item.heal_amount)
            health_healed = state.agent.health - health_healed
            state.agent.inventory.remove(heal_item)
            state.agent.inventory_qtt[1] -= 1
            state.agent.status[2] = 0
            state.medkits_used += 1
            if(state.prints_enabled):
                print(f"You used a medkit and healed {heal_item.heal_amount} health. Current health: {state.agent.health}") # type: ignore
            if state.medkits_used == 1:
                return state.achievement_reward + health_healed * 6
            if health_healed == heal_item.heal_amount:
                return health_healed * 6
            return health_healed * 3 
        else:
            if(state.prints_enabled):
                print("You need to have a medkit in the inventory to heal.")
            return state.invalid_return_value