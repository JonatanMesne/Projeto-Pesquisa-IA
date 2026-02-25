from items.item import Item
from actions.item_actions.heal import Heal

class Medkit(Item):
    def __init__(self):
        super().__init__(appearence='m', action=[Heal], inventory_space=2)
        self.heal_amount = 5