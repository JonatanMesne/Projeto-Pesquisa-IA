from items.item import Item
from actions.item_actions.drink import Drink

class Water(Item):
    def __init__(self):
        super().__init__(appearence='a', action=[Drink], inventory_space=1)
        self.thirst_satiation = 40
        
    def item_info(self) -> str:
        return f"Water: Satiates {self.thirst_satiation} thirst | Inventory Space: {self.inventory_space}"