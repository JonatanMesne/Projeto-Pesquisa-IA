from actions.action import Action

class UpdateVision(Action):     #class for the action of perceiving the surroundings
    duration = 0
    id = -1

    @staticmethod
    def action(state) -> bool:
        if state.action_zombie is not None:
            entity = state.action_zombie
        else:
            entity = state.agent
        vision_data = []
        id_vision_data = []
        check_pos = entity.position.copy()
        vision_range = entity.vision_range
        lost_vision = [0, 0]
        
        check_pos[0] = check_pos[0] - vision_range
        check_pos[1] = check_pos[1] - vision_range
        
        if (check_pos[0] < 0):
            lost_vision[0] = check_pos[0]
            check_pos[0] = 0
        if (check_pos[1] < 0):
            lost_vision[1] = check_pos[1]
            check_pos[1] = 0

        for i in range(vision_range * 2 + 1 + lost_vision[0]):
            vision_data.append([])
            id_vision_data.append([])
            for j in range(vision_range * 2 + 1 + lost_vision[1]):
                current_pos = [check_pos[0] + i, check_pos[1] + j]
                if (current_pos[0] >= len(state.world.grid) or
                    current_pos[1] >= len(state.world.grid[0])):
                    break
                else:
                    vision_data[i].append(state.world.grid[current_pos[0]][current_pos[1]])
                    id_vision_data[i].append(state.world.id_grid[current_pos[0]][current_pos[1]])

        entity.vision_data = vision_data
        entity.id_vision_data = id_vision_data
        return True