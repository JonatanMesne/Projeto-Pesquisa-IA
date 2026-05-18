from actions.action import Action
from items.ammo import Ammo
from items.food import Food
from items.item import Item
from items.medkit import Medkit
from items.water import Water
from items.weapons.ranged import RangedWeapon
from items.weapons.melee import MeleeWeapon
from world_objects.ground import Ground

class PickupItem(Action):   #class for picking up items
    duration = 1
    id = 21
    
    return_value = 100
        
    @staticmethod
    def action(state) -> int:
        if isinstance(state.agent.standing_on, Item):
            item_to_pickup = state.agent.standing_on
            
            if isinstance(item_to_pickup, RangedWeapon):
                if state.agent.ranged_weapon is not None:
                    state.agent.standing_on = state.agent.ranged_weapon
                state.agent.ranged_weapon = item_to_pickup
                return PickupItem.return_value
            elif isinstance(item_to_pickup, MeleeWeapon):
                if state.agent.melee_weapon is not None:
                    state.agent.standing_on = state.agent.melee_weapon
                state.agent.melee_weapon = item_to_pickup
                return PickupItem.return_value
            elif isinstance(item_to_pickup, Ammo):  # Handle ammo stacking
                ammo_to_pickup = item_to_pickup.ammo_count # type: ignore
                
                return_true = False
                
                # Try to fill existing ammo stacks in inventory
                for inventory_item in state.agent.inventory:
                    if isinstance(inventory_item, Ammo):
                        space_in_stack = inventory_item.stack_size - inventory_item.ammo_count
                        if space_in_stack > 0:
                            amount_to_add = min(space_in_stack, ammo_to_pickup)
                            inventory_item.ammo_count += amount_to_add
                            ammo_to_pickup -= amount_to_add
                            return_true = True  # At least some ammo was picked up
                            
                            if ammo_to_pickup == 0:
                                # All ammo transferred to existing stacks
                                state.agent.standing_on = Ground()
                
                # If there's remaining ammo, create a new stack if there's inventory space
                if ammo_to_pickup > 0:
                    if state.agent.inventory_qtt[0] < state.agent.max_inventory_qtt[0]:  # Check if there's space for another ammo stack
                        # Create a new ammo stack with remaining ammo
                        new_ammo_stack = Ammo()
                        new_ammo_stack.ammo_count = ammo_to_pickup
                        state.agent.inventory.append(new_ammo_stack)
                        state.agent.inventory_qtt[0] += 1
                        state.agent.standing_on = Ground()
                        if(state.prints_enabled):
                            print(f"You picked up: {item_to_pickup.__class__.__name__} (stack of {ammo_to_pickup} ammo)")
                        return PickupItem.return_value
                if return_true:
                    if(state.prints_enabled):
                        print(f"You picked up: {item_to_pickup.__class__.__name__} (added to existing stacks)")
                    return PickupItem.return_value
                else:
                    if(state.prints_enabled):
                        print("Cannot pick up ammo: inventory is full.")
                    return state.invalid_return_value  # Inventory is full
            else:
                # Handle regular items (non-ammo)
                inventory_index = 0
                if isinstance(item_to_pickup, Medkit):
                    inventory_index = 1
                elif isinstance(item_to_pickup, Food):
                    inventory_index = 2
                elif isinstance(item_to_pickup, Water):
                    inventory_index = 3
                if state.agent.inventory_qtt[inventory_index] < state.agent.max_inventory_qtt[inventory_index]:
                    state.agent.inventory.append(item_to_pickup)
                    state.agent.inventory_qtt[inventory_index] += 1
                    # Remove the item from the map grid
                    state.agent.standing_on = Ground()  # the agent is now standing on an empty ground tile
                    if(state.prints_enabled):
                        print(f"You picked up: {item_to_pickup.__class__.__name__}")
                    return PickupItem.return_value
                else:
                    if(state.prints_enabled):
                        print("Cannot pick up item: inventory is full.")
                    return state.invalid_return_value  # Inventory is full
        else:
            if(state.prints_enabled):
                print("No item to pick up here.")
            return state.invalid_return_value  # No item to pick up