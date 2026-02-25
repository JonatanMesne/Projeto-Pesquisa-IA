from actions.action import Action
from items.weapons.ranged import RangedWeapon
from items.weapons.melee import MeleeWeapon
from entities.entity import Entity
from world_objects.ground import Ground

class Attack(Action):     #class for the action of perceiving the surroundings
    def __init__(self):
        super().__init__(1) #action takes 1 time units

    @staticmethod
    def action(state) -> bool:
        hit = False
        if not isinstance(state.agent.item_in_hand, (MeleeWeapon, RangedWeapon)):
            pierce = 99
            fire_rate = 1
            damage = 5
            weapon_range = 1
            knockback = 1
        else:
            weapon_range = state.agent.item_in_hand.range
            damage = state.agent.item_in_hand.damage
            if isinstance(state.agent.item_in_hand, RangedWeapon):
                if state.agent.item_in_hand.ammo > 0:
                    pierce = state.agent.item_in_hand.pierce
                    fire_rate = state.agent.item_in_hand.fire_rate
                    knockback = 0
                else:
                    return False  # No ammo, cannot attack
            else:
                pierce = 99
                fire_rate = 1
                knockback = state.agent.item_in_hand.knockback
        direction_array = [0, 0]
        if state.entity_direction == 1:
            direction_array[0] -= 1
        elif state.entity_direction == 2:
            direction_array[1] += 1
        elif state.entity_direction == 3:
            direction_array[0] += 1
        elif state.entity_direction == 4:
            direction_array[1] -= 1
        for _ in range(fire_rate):
            # track entities hit this shot (in order from nearest to farthest)
            hits = []  # list of (entity, position)
            if isinstance(state.agent.item_in_hand, RangedWeapon):
                state.agent.item_in_hand.ammo -= 1
            for j in range(weapon_range):
                target_position = [state.agent.position[0] + direction_array[0] * (j + 1), 
                                   state.agent.position[1] + direction_array[1] * (j + 1)]
                if (target_position[0] < 0 or target_position[0] >= len(state.map_grid) or
                    target_position[1] < 0 or target_position[1] >= len(state.map_grid[0])):
                    break  # Out of bounds
                target_cell = state.map_grid[target_position[0]][target_position[1]]
                if isinstance(target_cell, Entity):
                    # apply damage
                    hit = True
                    target_cell.health -= damage
                    pierce -= 1
                    if target_cell.health <= 0:
                        # entity died — remove from map
                        state.entity_death(target_cell)
                    # record hit (store entity reference)
                    hits.append(target_cell)
                    if pierce <= 0:
                        break
                    continue  # Continue checking further if pierce > 0
                if target_cell.is_solid:
                    hit = True
                    target_cell.durability -= damage // 4  # Walls take reduced damage
                    if target_cell.durability <= 0:
                        state.map_grid[target_position[0]][target_position[1]] = Ground()  # Replace with a passable ground tile
                    break  # Hit a wall, stop checking further

            # apply knockback for this shot's hits, from farthest to nearest
            if knockback > 0 and len(hits) > 0:
                for entity in reversed(hits):
                    # attempt to push the entity away from attacker up to knockback tiles
                    for _k in range(knockback):
                        new_x = entity.position[0] + direction_array[0]
                        new_y = entity.position[1] + direction_array[1]
                        # check bounds
                        if (new_x < 0 or new_x >= len(state.map_grid) or
                            new_y < 0 or new_y >= len(state.map_grid[0])):
                            break
                        target_cell = state.map_grid[new_x][new_y]
                        # stop if blocked by a solid tile or another entity
                        if target_cell.is_solid:
                            break
                        # move entity: set current cell to its standing_on, place entity in new cell
                        state.map_grid[entity.position[0]][entity.position[1]] = entity.standing_on
                        entity.place_entity(state.map_grid, [new_x, new_y])  # Update entity's position on the grid
        return hit