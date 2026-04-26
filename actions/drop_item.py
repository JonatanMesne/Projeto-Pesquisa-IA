from actions.action import Action
from items.ammo import Ammo
from world_objects.ground import Ground

class DropItem(Action):     #class for the action of dropping an item from the agent's inventory
    duration = 0
    need_index = True
    id = 200 #to 200 + agent_inventory

    @staticmethod
    def action(state) -> bool:
        index = state.current_action_id - DropItem.id  # Calculate index based on action ID
        item_dropped = state.agent.inventory[index] if index >= 0 and index < len(state.agent.inventory) else None
        if item_dropped is not None:
            if state.agent.item_in_hand == item_dropped:
                state.agent.item_in_hand = None  # If the dropped item is currently held, empty the hands
            if isinstance(state.agent.standing_on, Ground):
                state.agent.standing_on = item_dropped  # Drop the item on the ground
            elif isinstance(state.agent.standing_on, Ammo) and isinstance(item_dropped, Ammo):
                state.agent.standing_on.ammo_count += min(item_dropped.ammo_count + state.agent.standing_on.ammo_count, item_dropped.stack_size)  # Stack ammo if dropping on existing ammo
            state.agent.inventory_space_used -= item_dropped.inventory_space
            state.agent.inventory.pop(index)
            print(f"You dropped: {item_dropped.__class__.__name__}")
            return True
        print("Invalid index. No item dropped.")
        return False