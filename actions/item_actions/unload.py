from actions.action import Action
from actions.pickup_item import PickupItem
from items.ammo import Ammo

class Unload(Action):   #class for unloading ammo from the item in hand
    duration = 1
        
    @staticmethod
    def action(state) -> bool:
        if(state.agent.item_in_hand.__class__.__name__ == "RangedWeapon"):
            weapon = state.agent.item_in_hand
            if weapon.__class__.__name__ == "RangedWeapon":
                if weapon.ammo > 0:
                    previous_ground = state.agent.standing_on
                    weapon_ammo = Ammo()
                    weapon_ammo.ammo_count = weapon.ammo
                    print(f"Unloaded {weapon_ammo.ammo_count} ammo from {weapon.__class__.__name__}.")
                    state.agent.standing_on = weapon_ammo
                    PickupItem.action(state)
                    if state.agent.standing_on.__class__.__name__ == "Ammo":
                        weapon.ammo = state.agent.standing_on.ammo_count
                    else:
                        weapon.ammo = 0
                    state.agent.standing_on = previous_ground
                    return True
            print("No ammo to unload or item in hand is not a ranged weapon.")
            return False