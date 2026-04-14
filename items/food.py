from items.item import Item
from actions.item_actions.eat import Eat

class Food(Item):
    id = 22
    def __init__(self):
        super().__init__(appearence='f', action=[Eat], inventory_space=1)
        self.hunger_satiation = 40
        
    def item_info(self) -> str:
        return f"Food: Satiates {self.hunger_satiation} hunger | Inventory Space: {self.inventory_space}"