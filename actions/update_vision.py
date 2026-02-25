from actions.action import Action

class UpdateVision(Action):     #class for the action of perceiving the surroundings
    def __init__(self):
        super().__init__(0) #action takes 0 time units

    @staticmethod
    def action(state) -> bool:
        if state.zombie is not None:
            entity = state.zombie
        else:
            entity = state.agent
        vision_data = []
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
            for j in range(vision_range * 2 + 1 + lost_vision[1]):
                current_pos = [check_pos[0] + i, check_pos[1] + j]
                if (current_pos[0] >= len(state.map_grid) or
                    current_pos[1] >= len(state.map_grid[0])):
                    break
                else:
                    vision_data[i].append(state.map_grid[current_pos[0]][current_pos[1]])

        entity.vision_data = vision_data
        return True