from actions.action import Action
from world_objects.world_object import WorldObject

class UpdateVision(Action):     #class for the action of perceiving the surroundings
    duration = 0
    id = -1

    @staticmethod
    def action(state) -> int:
        if state.action_zombie is not None:
            entity = state.action_zombie
        else:
            entity = state.agent
        vision_data = []
        id_vision_data = []
        check_pos = entity.position.copy()
        vision_range = entity.vision_range
        
        check_pos[0] = check_pos[0] - vision_range
        check_pos[1] = check_pos[1] - vision_range

        for i in range(vision_range * 2 + 1):
            vision_data.append([])
            id_vision_data.append([])
            for j in range(vision_range * 2 + 1):
                current_pos = [check_pos[0] + i, check_pos[1] + j]
                if (current_pos[0] < 0 or current_pos[1] < 0 or
                    current_pos[0] >= len(state.world.grid) or
                    current_pos[1] >= len(state.world.grid[0])):
                    vision_data[i].append(WorldObject())   #if the position is out of bounds, consider it an invalid world object
                    id_vision_data[i].append(0)   #id 0 is reserved for invalid world objects
                else:
                    vision_data[i].append(state.world.grid[current_pos[0]][current_pos[1]])
                    id_vision_data[i].append(state.world.grid[current_pos[0]][current_pos[1]].id)

        entity.vision_data = vision_data
        entity.id_vision_data = id_vision_data
        return 0