from actions.action import Action
from actions.pickup_item import PickupItem
from items.ammo import Ammo
from items.weapons.ranged import RangedWeapon

class Unload(Action):   #class for unloading ammo from the item in hand
    duration = 1
    id = 25
        
    @staticmethod
    def action(state) -> bool:
        weapon = state.agent.item_in_hand
        if isinstance(weapon, RangedWeapon):
            if weapon.ammo > 0:
                previous_ground = state.agent.standing_on
                weapon_ammo = Ammo()
                weapon_ammo.ammo_count = weapon.ammo
                print(f"Unloaded {weapon_ammo.ammo_count} ammo from {weapon.__class__.__name__}.")
                state.agent.standing_on = weapon_ammo
                PickupItem.action(state)
                if isinstance(state.agent.standing_on, Ammo):
                    weapon.ammo = state.agent.standing_on.ammo_count
                else:
                    weapon.ammo = 0
                state.agent.standing_on = previous_ground
                return True
        print("No ammo to unload or item in hand is not a ranged weapon.")
        return False