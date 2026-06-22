from entities.entity import Entity
from actions.action import Action
from items.weapons.melee import MeleeWeapon
from items.weapons.ranged import RangedWeapon
from world_objects.ground import Ground

class Attack(Action):     #class for the action of perceiving the surroundings
    duration = 1
    need_direction = True
    id = 22  #to 
    
    failed_attack_return_value = -500

    @staticmethod
    def action(state) -> int:
        hit = False
        damage_total = 0           # keep track of total damage dealt
        entity_direction = (state.current_action_id - Attack.id) % 4  # Calculate direction based on action ID

        if state.current_action_id > Attack.id + 3:
            weapon = state.agent.ranged_weapon
            if weapon is None:
                if(state.prints_enabled):
                    print("Attack failed: no ranged weapon equipped.")
                return state.invalid_return_value
            if weapon.ammo <= 0:
                if(state.prints_enabled):
                    print("Attack failed: no ammo.")
                return state.invalid_return_value  # No ammo, cannot attack
            
            weapon_range = weapon.range
            damage = weapon.damage
            pierce = weapon.pierce
            fire_rate = weapon.fire_rate
            knockback = 0
        elif state.agent.melee_weapon is not None:
            weapon_range = state.agent.melee_weapon.range
            damage = state.agent.melee_weapon.damage
            pierce = 99
            fire_rate = 1
            knockback = state.agent.melee_weapon.knockback
        else:
            pierce = 99
            fire_rate = 1
            damage = 5
            weapon_range = 1
            knockback = 1

        direction_array = [0, 0]
        #direction = 0 (up) | 1 (right) | 2 (down) | 3 (left)
        if entity_direction == 0:
            direction_array[0] -= 1
        elif entity_direction == 1:
            direction_array[1] += 1
        elif entity_direction == 2:
            direction_array[0] += 1
        elif entity_direction == 3:
            direction_array[1] -= 1

        for _ in range(fire_rate):
            # track entities hit this shot (in order from nearest to farthest)
            hits = []  # list of (entity, position)
            if state.current_action_id > Attack.id + 3:
                state.agent.ranged_weapon.ammo -= 1
            for j in range(weapon_range):
                target_position = [state.agent.position[0] + direction_array[0] * (j + 1), 
                                   state.agent.position[1] + direction_array[1] * (j + 1)]
                if (target_position[0] < 0 or target_position[0] >= len(state.world.grid) or
                    target_position[1] < 0 or target_position[1] >= len(state.world.grid[0])):
                    if j == 0:
                        return state.invalid_return_value  # Attack in invalid direction
                    else:
                        break  # Out of bounds
                target_cell = state.world.grid[target_position[0]][target_position[1]]
                if isinstance(target_cell, Entity):
                    # apply damage
                    hit = True
                    target_cell.health -= damage
                    damage_total += damage
                    pierce -= 1
                    if target_cell.health <= 0:
                        return_value = 0
                        if state.current_action_id > Attack.id + 3:
                            state.ranged_kills += 1
                            for i in range(len(state.ranged_kills_achievement_thresholds)):
                                if state.ranged_kills == state.ranged_kills_achievement_thresholds[i]:
                                    state.ranged_achievement_count += 1
                                    return_value += (state.achievement_reward * (i + 1))
                                    break
                        else:
                            state.melee_kills += 1
                            for i in range(len(state.melee_kills_achievement_thresholds)):
                                if state.melee_kills == state.melee_kills_achievement_thresholds[i]:
                                    state.melee_achievement_count += 1
                                    return_value += (state.achievement_reward * (i + 1))
                                    break
                        # entity died — remove from map
                        if state.entity_death(target_cell) == 10:  # Zombie death
                            achievement = False
                            for i in range(len(state.zombies_killed_achievement_thresholds)):
                                if state.zombies_killed == state.zombies_killed_achievement_thresholds[i]:
                                    state.zombie_achievement_count += 1
                                    return_value += (state.achievement_reward * (i + 1))
                                    achievement = True
                                    break
                            if not achievement:
                                return_value += 100
                        damage_total += return_value // 10  # Convert back to damage for consistent return value
                        if(state.prints_enabled):
                            print(f"{target_cell.__class__.__name__} has been defeated.")
                    else:
                        # record hit (store entity reference)
                        hits.append(target_cell)
                    if pierce <= 0:
                        break
                    continue  # Continue checking further if pierce > 0
                if target_cell.is_solid:
                    hit = True
                    dmg = damage // 4  # Walls take reduced damage
                    if dmg <= 0:
                        dmg = 1  # Ensure at least 1 damage is dealt to walls
                    target_cell.durability -= dmg
                    # damage_total += 0.1 
                    if target_cell.durability <= 0:
                        state.world.grid[target_position[0]][target_position[1]] = Ground()  # Replace with a passable ground tile
                        if(state.prints_enabled):
                            print("You destroyed a wall!")
                    break  # Hit a wall, stop checking further

            # apply knockback for this shot's hits, from farthest to nearest
            if knockback > 0 and len(hits) > 0:
                for entity in reversed(hits):
                    # attempt to push the entity away from attacker up to knockback tiles
                    for _k in range(knockback):
                        new_x = entity.position[0] + direction_array[0]
                        new_y = entity.position[1] + direction_array[1]
                        # check bounds
                        if (new_x < 0 or new_x >= len(state.world.grid) or
                            new_y < 0 or new_y >= len(state.world.grid[0])):
                            break
                        target_cell = state.world.grid[new_x][new_y]
                        # stop if blocked by a solid tile or another entity
                        if target_cell.is_solid:
                            break
                        # move entity: set current cell to its standing_on, place entity in new cell
                        state.world.grid[entity.position[0]][entity.position[1]] = entity.standing_on
                        entity.place_entity(state.world.grid, [new_x, new_y])  # Update entity's position on the grid

        if not hit:
            if(state.prints_enabled):
                print("Your attack missed.")
            return Attack.failed_attack_return_value

        if(state.prints_enabled):
            print(f"You dealt {damage_total} total damage.")
        return int(damage_total * 10)