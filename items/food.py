from items.item import Item

class Food(Item):
    id = 22
    def __init__(self):
        super().__init__(appearence='f')
        self.hunger_satiation = 40
        
    def item_info(self) -> str:
        return f"Food: Satiates {self.hunger_satiation} hunger"