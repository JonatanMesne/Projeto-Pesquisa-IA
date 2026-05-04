from actions.action import Action

class DoorAction(Action):   #class for opening and closing doors
    duration = 1
    need_direction = True
    id = 17 #to 20
        
    @staticmethod
    def action(state) -> int:
        direction = state.current_action_id - DoorAction.id  # Calculate direction based on action ID
        WO_position = state.agent.position.copy()
        #direction = 0 (up) | 1 (right) | 2 (down) | 3 (left)
        if direction == 0:
            WO_position[0] -= 1
        elif direction == 1:
            WO_position[1] += 1
        elif direction == 2:
            WO_position[0] += 1
        elif direction == 3:
            WO_position[1] -= 1
        if (WO_position[0] < 0 or WO_position[0] >= len(state.world.grid) or
            WO_position[1] < 0 or WO_position[1] >= len(state.world.grid[0])):
            # print("Invalid move to position:", next_position)
            return state.invalid_return_value
        world_object = state.world.grid[WO_position[0]][WO_position[1]]
        
        if world_object.__class__.__name__ == 'Door':
            #Toggle door state between open and closed
            if(world_object.is_solid == True):
                world_object.appearence = 'd'  #Open door
                world_object.is_solid = False
                world_object.id = 15  #Change ID to represent open door
            else:
                world_object.appearence = 'D'  #Closed door
                world_object.is_solid = True
                world_object.id = 14  #Change ID back to represent closed door
            if(state.prints_enabled):
                print(f"You {'opened' if not world_object.is_solid else 'closed'} the door.")
            return 0
        else:
            if(state.prints_enabled):
                print("There is no door in that direction.")
            return state.invalid_return_value