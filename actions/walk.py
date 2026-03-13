from actions.action import Action

class Walk(Action):     #class for the action of walking 1 tile
    duration = 1
    need_direction = True

    @staticmethod
    def action(state) -> bool:
        if state.action_zombie is not None:
            entity = state.action_zombie
        else:
            entity = state.agent
        next_position = entity.position.copy()
        # print("Attempting to walk in direction:", state.entity_direction)
        #direction = 1 (up) | 2 (right) | 3 (down) | 4 (left)
        if state.entity_direction == 1:
            next_position[0] -= 1
        elif state.entity_direction == 2:
            next_position[1] += 1
        elif state.entity_direction == 3:
            next_position[0] += 1
        elif state.entity_direction == 4:
            next_position[1] -= 1
        else:
            print("Invalid direction:", state.entity_direction)
            return False
        #Check if next position is valid
        if (next_position[0] < 0 or next_position[0] >= len(state.world.grid) or
            next_position[1] < 0 or next_position[1] >= len(state.world.grid[0]) or 
            (state.world.grid[next_position[0]][next_position[1]].is_solid and not entity.standing_on.is_solid)):
            # print("Invalid move to position:", next_position)
            return False
        #Move entity to next position, restoring the ground it was standing on and updating where the entity is standing
        state.world.grid[entity.position[0]][entity.position[1]] = entity.standing_on
        entity.standing_on = state.world.grid[next_position[0]][next_position[1]]
        state.world.grid[next_position[0]][next_position[1]] = entity
        entity.position = next_position
        # print("Walked to position:", entity.position)
        return True
        
