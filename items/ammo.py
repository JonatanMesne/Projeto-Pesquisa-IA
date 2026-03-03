from items.item import Item

class Ammo(Item):
    def __init__(self):
        super().__init__(appearence='a', action=None, inventory_space=1, has_action=False)
        self.ammo_count = 30
        self.stack_size = 60
        
    def item_info(self) -> str:
        return f"Ammo: {self.ammo_count}/{self.stack_size} | Inventory Space: {self.inventory_space}"