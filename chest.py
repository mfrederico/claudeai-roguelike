from items import generate_random_item
import config

class Chest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.char = 'C'
        self.color = config.CHEST_COLOR
        self.item = generate_random_item()
