from items.item import Item

class Medkit(Item):
    id = 24
    def __init__(self):
        super().__init__(appearence='m')
        self.heal_amount = 30
        
    def item_info(self) -> str:
        return f"Medkit: Heals {self.heal_amount} health"