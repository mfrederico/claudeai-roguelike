import random
import config

class Item:
    def __init__(self, name, char, color):
        self.name = name
        self.char = char
        self.color = color

    def use(self, entity):
        pass

    def get_description(self):
        return f"{self.name}"

class Armor(Item):
    def __init__(self, armor_type):
        super().__init__(armor_type, 'A', config.COLOR_PLAYER)
        self.armor_type = armor_type
        self.protection = config.ARMOR_TYPES[armor_type]

    def use(self, entity):
        if hasattr(entity, 'equip_armor'):
            return entity.equip_armor(self.armor_type)
        return f"{entity.name} can't equip armor."

    def get_description(self):
        return f"{self.armor_type} Armor (Protection: {self.protection * 100:.0f}%)"

def generate_random_item():
    item_type = random.choices(list(config.TREASURE_TYPES.keys()), 
                               weights=list(config.TREASURE_TYPES.values()))[0]
    if item_type == 'armor':
        armor_type = random.choice(list(config.ARMOR_TYPES.keys()))
        return Armor(armor_type)
    # Add more item types here in the future
    return None

class Weapon(Item):
    def __init__(self, weapon_type):
        super().__init__(weapon_type, 'W', config.COLOR_PLAYER)
        self.weapon_type = weapon_type
        self.bonus = config.WEAPON_TYPES[weapon_type]

    def use(self, entity):
        if hasattr(entity, 'equip_weapon'):
            return entity.equip_weapon(self)
        return f"{entity.name} can't equip weapons."

    def get_description(self):
        if self.bonus == 'instant':
            return f"{self.weapon_type} (Instant Kill)"
        return f"{self.weapon_type} (Attack Bonus: +{self.bonus * 100:.0f}%)"

def generate_random_item():
    item_type = random.choices(list(config.TREASURE_TYPES.keys()),
                               weights=list(config.TREASURE_TYPES.values()))[0]
    if item_type == 'armor':
        armor_type = random.choice(list(config.ARMOR_TYPES.keys()))
        return Armor(armor_type)
    elif item_type == 'weapon':
        weapon_type = random.choice(list(config.WEAPON_TYPES.keys()))
        return Weapon(weapon_type)
    return None
