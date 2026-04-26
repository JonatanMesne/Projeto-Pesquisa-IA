from actions.action import Action

class DoorAction(Action):   #class for opening and closing doors
    duration = 1
    need_direction = True
    id = 17 #to 20
        
    @staticmethod
    def action(state) -> bool:
        direction = state.current_action_id - DoorAction.id  # Calculate direction based on action ID
        world_object = state.get_world_object_in_front(direction)
        if world_object.action.__name__ == 'DoorAction':
            #Toggle door state between open and closed
            if(world_object.is_solid == True):
                world_object.appearence = 'd'  #Open door
                world_object.is_solid = False
            else:
                world_object.appearence = 'D'  #Closed door
                world_object.is_solid = True
            print(f"You {'opened' if not world_object.is_solid else 'closed'} the door.")
            return True
        else:
            print("There is no door in that direction.")
            return False