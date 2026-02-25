from actions.action import Action
from items.ammo import Ammo

class Reload(Action):     #class for the action of reloading a weapon
    def __init__(self):
        super().__init__(1) #action takes 1 time unit

    @staticmethod
    def action(state) -> bool:
        # Must have a ranged weapon in hand
        weapon = state.agent.item_in_hand

        # Already full
        needed = weapon.ammo_capacity - weapon.ammo
        if needed <= 0:
            return False

        transferred = 0

        # Iterate over a copy since we may remove empty stacks
        for inv_item in state.agent.inventory[:]:
            if not isinstance(inv_item, Ammo):
                continue
            if inv_item.ammo_count <= 0:
                # remove empty stacks if any
                state.agent.remove_item(inv_item)
                continue

            take = min(inv_item.ammo_count, needed)
            weapon.ammo += take
            inv_item.ammo_count -= take
            needed -= take
            transferred += take

            # remove stack if emptied
            if inv_item.ammo_count == 0:
                state.agent.remove_item(inv_item)

            if needed == 0:
                break

        if transferred > 0:
            state.advance_time()
            return True

        return False