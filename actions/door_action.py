from actions.action import Action

class DoorAction(Action):   #class for opening and closing doors
    duration = 1
    need_direction = True
        
    @staticmethod
    def action(state) -> bool:
        world_object = state.get_world_object_in_front()
        if world_object.action.__name__ == 'DoorAction':
            #Toggle door state between open and closed
            if(world_object.is_solid == True):
                world_object.appearence = 'd'  #Open door
                world_object.is_solid = False
                world_object.id = 15  #Change ID to represent open door
                state.world.id_grid[world_object.position[0]][world_object.position[1]] = world_object.id  #Update the world's ID grid to reflect the door's new state
            else:
                world_object.appearence = 'D'  #Closed door
                world_object.is_solid = True
                world_object.id = 14  #Change ID back to represent closed door
                state.world.id_grid[world_object.position[0]][world_object.position[1]] = world_object.id  #Update the world's ID grid to reflect the door's new state
            print(f"You {'opened' if not world_object.is_solid else 'closed'} the door.")
            return True
        else:
            print("There is no door in that direction.")
            return False