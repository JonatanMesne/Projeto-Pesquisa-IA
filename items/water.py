from items.item import Item

class Water(Item):
    id = 21
    def __init__(self):
        super().__init__(appearence='w')
        self.thirst_satiation = 40
        
    def item_info(self) -> str:
        return f"Water: Satiates {self.thirst_satiation} thirst"