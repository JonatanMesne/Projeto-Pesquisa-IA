from actions.action import Action

class Walk(Action):     #class for the action of walking 1 tile
    duration = 1
    need_direction = True
    id = 1  #to 4

    @staticmethod
    def action(state) -> bool:
        entity_direction = state.current_action_id - Walk.id  # Calculate direction based on action ID
        if state.action_zombie is not None:
            entity = state.action_zombie
        else:
            entity = state.agent
        next_position = entity.position.copy()
        # print("Attempting to walk in direction:", entity_direction)
        #direction = 0 (up) | 1 (right) | 2 (down) | 3 (left)
        if entity_direction == 0:
            next_position[0] -= 1
        elif entity_direction == 1:
            next_position[1] += 1
        elif entity_direction == 2:
            next_position[0] += 1
        elif entity_direction == 3:
            next_position[1] -= 1
        else:
            print("Invalid direction:", entity_direction)
            return False
        #Check if next position is not valid
        if (next_position[0] < 0 or next_position[0] >= len(state.world.grid) or
            next_position[1] < 0 or next_position[1] >= len(state.world.grid[0]) or 
            (state.world.grid[next_position[0]][next_position[1]].is_solid and not entity.standing_on.is_solid)):
            # print("Invalid move to position:", next_position)
            return False
        #Move entity to next position, restoring the ground it was standing on and updating where the entity is standing
        state.world.grid[entity.position[0]][entity.position[1]] = entity.standing_on
        state.world.id_grid[entity.position[0]][entity.position[1]] = entity.standing_on.id
        entity.standing_on = state.world.grid[next_position[0]][next_position[1]]
        state.world.grid[next_position[0]][next_position[1]] = entity
        state.world.id_grid[next_position[0]][next_position[1]] = entity.id
        entity.position = next_position
        # print("Walked to position:", entity.position)
        return True
        
