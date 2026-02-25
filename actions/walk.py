from actions.action import Action

class Walk(Action):     #class for the action of walking 1 tile
    def __init__(self):
        super().__init__(1) #action takes 1 time unit

    @staticmethod
    def action(state) -> bool:
        state.advance_time()
        if state.zombie is not None:
            entity = state.zombie
        else:
            entity = state.agent
        next_position = entity.position.copy()
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
            return False
        #Check if next position is valid
        if (next_position[0] < 0 or next_position[0] >= len(state.map_grid) or
            next_position[1] < 0 or next_position[1] >= len(state.map_grid[0]) or 
            state.map_grid[next_position[0]][next_position[1]].is_solid):
            return False
        #Move entity to next position, restoring the ground it was standing on and updating where the entity is standing
        state.map_grid[entity.position[0]][entity.position[1]] = entity.standing_on
        entity.standing_on = state.map_grid[next_position[0]][next_position[1]]
        state.map_grid[next_position[0]][next_position[1]] = entity
        entity.position = next_position
        state.entity_direction = 0
        return True
        
