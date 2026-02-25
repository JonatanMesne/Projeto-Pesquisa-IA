from actions.action import Action
from items.item import Item
from items.ammo import Ammo
from world_objects.ground import Ground

class PickupItem(Action):   #class for picking up items
    def __init__(self):
        super().__init__(1) #action takes 1 time unit
        
    @staticmethod
    def action(state) -> bool:
        state.advance_time()
        if isinstance(state.agent.standing_on, Item):
            item_to_pickup = state.agent.standing_on
            
            # Handle ammo stacking
            if isinstance(item_to_pickup, Ammo):
                ammo_to_pickup = item_to_pickup.ammo_count
                
                return_value = False
                
                # Try to fill existing ammo stacks in inventory
                for inventory_item in state.agent.inventory:
                    if isinstance(inventory_item, Ammo):
                        space_in_stack = inventory_item.stack_size - inventory_item.ammo_count
                        if space_in_stack > 0:
                            amount_to_add = min(space_in_stack, ammo_to_pickup)
                            inventory_item.ammo_count += amount_to_add
                            ammo_to_pickup -= amount_to_add
                            return_value = True  # At least some ammo was picked up
                            
                            if ammo_to_pickup == 0:
                                # All ammo transferred to existing stacks
                                state.agent.standing_on = Ground()
                                return return_value
                
                # If there's remaining ammo, create a new stack if there's inventory space
                if ammo_to_pickup > 0:
                    if state.agent.inventory_space_used + item_to_pickup.inventory_space <= state.agent.max_inventory_space:
                        # Create a new ammo stack with remaining ammo
                        new_ammo_stack = Ammo()
                        new_ammo_stack.ammo_count = ammo_to_pickup
                        state.agent.inventory.append(new_ammo_stack)
                        state.agent.inventory_space_used += new_ammo_stack.inventory_space
                        state.agent.standing_on = Ground()
                        return True
                return return_value  # Inventory is full
            else:
                # Handle regular items (non-ammo)
                if state.agent.inventory_space_used + item_to_pickup.inventory_space <= state.agent.max_inventory_space:
                    state.agent.inventory.append(item_to_pickup)
                    state.agent.inventory_space_used += item_to_pickup.inventory_space
                    # Remove the item from the map grid
                    state.agent.standing_on = Ground()  # the agent is now standing on an empty ground tile
                    return True
                else:
                    return False  # Inventory is full
        else:
            return False  # No item to pick up