from actions.action import Action
from items.ammo import Ammo
from items.weapons.ranged import RangedWeapon

class Reload(Action):     #class for the action of reloading a weapon
    duration = 1
    id = 20

    @staticmethod
    def action(state) -> int:
        weapon = state.agent.ranged_weapon
        if isinstance(weapon, RangedWeapon):
            needed = weapon.ammo_capacity - weapon.ammo
            if needed <= 0:     # Already full
                if(state.prints_enabled):
                    print("Your weapon is already fully loaded.")
                return state.invalid_return_value

            transferred = 0

            # Iterate over a copy since we may remove empty stacks
            for inv_item in state.agent.inventory[:]:
                if not isinstance(inv_item, Ammo):
                    continue

                take = min(inv_item.ammo_count, needed)
                weapon.ammo += take
                inv_item.ammo_count -= take
                needed -= take
                transferred += take

                # remove stack if emptied
                if inv_item.ammo_count == 0:
                    state.agent.inventory.remove(inv_item)
                    state.agent.inventory_qtt[0] -= 1

                if needed == 0:
                    break

            if transferred > 0:
                if(state.prints_enabled):
                    print(f"You reloaded your {weapon.__class__.__name__} with {transferred} ammo. Current ammo: {weapon.ammo}/{weapon.ammo_capacity}")
                return 20
            if(state.prints_enabled):
                print("You don't have any ammo to reload your weapon.")
            return state.invalid_return_value
        else:
            if(state.prints_enabled):
                print("You need to have a ranged weapon in hand to reload.")
            return state.invalid_return_value