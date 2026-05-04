from actions.action import Action
from actions.pickup_item import PickupItem
from items.ammo import Ammo

class Unload(Action):   #class for unloading ammo from the item in hand
    duration = 1
    id = 25
        
    @staticmethod
    def action(state) -> int:
        weapon = state.agent.item_in_hand
        if any(base.__name__ == "RangedWeapon" for base in type(weapon).mro()): #check if item in hand is a ranged weapon (or subclass of)
            if weapon.ammo > 0:
                previous_ground = state.agent.standing_on
                weapon_ammo = Ammo()
                weapon_ammo.ammo_count = weapon.ammo
                if(state.prints_enabled):
                    print(f"Unloaded {weapon_ammo.ammo_count} ammo from {weapon.__class__.__name__}.")
                state.agent.standing_on = weapon_ammo
                PickupItem.action(state)
                if state.agent.standing_on.__class__.__name__ == "Ammo":
                    weapon.ammo = state.agent.standing_on.ammo_count
                else:
                    weapon.ammo = 0
                state.agent.standing_on = previous_ground
                return 0
            if(state.prints_enabled):
                print("No ammo to unload or item in hand is not a ranged weapon.")
        return state.invalid_return_value