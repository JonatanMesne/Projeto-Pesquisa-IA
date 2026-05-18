from items.item import Item

class Ammo(Item):
    id = 23
    def __init__(self):
        super().__init__(appearence='a')
        self.ammo_count = 30
        self.stack_size = 60
        
    def item_info(self) -> str:
        return f"Ammo: {self.ammo_count}/{self.stack_size}"