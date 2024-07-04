import random
import config

class Item:
    def __init__(self, name, char, color):
        self.name = name
        self.char = char
        self.color = color

    def use(self, entity):
        pass

class Armor(Item):
    def __init__(self, armor_type):
        super().__init__(armor_type, 'A', config.COLOR_PLAYER)
        self.armor_type = armor_type
        self.protection = config.ARMOR_TYPES[armor_type]

    def use(self, entity):
        if hasattr(entity, 'equip_armor'):
            return entity.equip_armor(self.armor_type)
        return f"{entity.name} can't equip armor."

def generate_random_item():
    item_type = random.choices(list(config.TREASURE_TYPES.keys()), 
                               weights=list(config.TREASURE_TYPES.values()))[0]
    if item_type == 'armor':
        armor_type = random.choice(list(config.ARMOR_TYPES.keys()))
        return Armor(armor_type)
    # Add more item types here in the future
    return None
