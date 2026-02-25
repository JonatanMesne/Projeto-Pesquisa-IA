from items.item import Item

class Ammo(Item):
    def __init__(self):
        super().__init__(appearence='a', action=None, inventory_space=1)
        self.ammo_count = 30
        self.stack_size = 60
        
    def print_status(self):
        print(f"Ammo: {self.ammo_count}/{self.stack_size}")