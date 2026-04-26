from actions.action import Action
from items.ammo import Ammo
from items.item import Item
from world_objects.ground import Ground

class PickupItem(Action):   #class for picking up items
    duration = 1
    id = 26
        
    @staticmethod
    def action(state) -> int:
        if isinstance(state.agent.standing_on, Item):
            item_to_pickup = state.agent.standing_on
            
            # Handle ammo stacking
            if item_to_pickup.__class__.__name__ == "Ammo":
                ammo_to_pickup = item_to_pickup.ammo_count # type: ignore
                
                return_value = False
                
                # Try to fill existing ammo stacks in inventory
                for inventory_item in state.agent.inventory:
                    if inventory_item.__class__.__name__ == "Ammo":
                        space_in_stack = inventory_item.stack_size - inventory_item.ammo_count
                        if space_in_stack > 0:
                            amount_to_add = min(space_in_stack, ammo_to_pickup)
                            inventory_item.ammo_count += amount_to_add
                            ammo_to_pickup -= amount_to_add
                            return_value = True  # At least some ammo was picked up
                            
                            if ammo_to_pickup == 0:
                                # All ammo transferred to existing stacks
                                state.agent.standing_on = Ground()
                                # return return_value
                
                # If there's remaining ammo, create a new stack if there's inventory space
                if ammo_to_pickup > 0:
                    if state.agent.inventory_space_used + item_to_pickup.inventory_space <= state.agent.max_inventory_space:
                        # Create a new ammo stack with remaining ammo
                        new_ammo_stack = Ammo()
                        new_ammo_stack.ammo_count = ammo_to_pickup
                        state.agent.inventory.append(new_ammo_stack)
                        state.agent.id_inventory.append(new_ammo_stack.id)
                        state.agent.inventory_space_used += new_ammo_stack.inventory_space
                        state.agent.standing_on = Ground()
                        print(f"You picked up: {item_to_pickup.__class__.__name__} (stack of {ammo_to_pickup} ammo)")
                        return 10
                if return_value:
                    print(f"You picked up: {item_to_pickup.__class__.__name__} (added to existing stacks)")
                    return 10
                else:
                    print("Cannot pick up ammo: inventory is full.")
                    return -100  # Inventory is full
            else:
                # Handle regular items (non-ammo)
                if state.agent.inventory_space_used + item_to_pickup.inventory_space <= state.agent.max_inventory_space:
                    state.agent.inventory.append(item_to_pickup)
                    state.agent.id_inventory.append(item_to_pickup.id)
                    state.agent.inventory_space_used += item_to_pickup.inventory_space
                    # Remove the item from the map grid
                    state.agent.standing_on = Ground()  # the agent is now standing on an empty ground tile
                    print(f"You picked up: {item_to_pickup.__class__.__name__}")
                    return 10
                else:
                    print("Cannot pick up item: inventory is full.")
                    return -100  # Inventory is full
        else:
            print("No item to pick up here.")
            return -100  # No item to pick up