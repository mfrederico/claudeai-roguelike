import math
import random
import config

class Entity:
    def __init__(self, x, y, char, name, color=config.COLOR_RESET):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.inventory = {
            'weapon': [None, None],
            'armor': None,
            'rings': [None, None],
            'boots': None,
            'helmet': None,
            'bag': []
        }
        self.attributes = {
            'power': config.PLAYER_STARTING_POWER,
            'magic': config.PLAYER_STARTING_MAGIC,
            'clarity': config.PLAYER_STARTING_CLARITY,
            'hit_points': config.PLAYER_STARTING_HP,
            'experience': 0,
            'level': 1
        }
        self.modifiers = {
            'PLM': 0,
            'ILM': 0,
            'MLM': 0,
            'CLM': 0,
            'ELM': 0
        }

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_hit_points(self):
        return round(self.attributes['hit_points'], 2)

    def set_hit_points(self, value):
        self.attributes['hit_points'] = round(value, 2)

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '@', 'Player', config.COLOR_PLAYER)
        self.fov_radius = config.PLAYER_FOV_RADIUS
        self.max_hit_points = config.PLAYER_STARTING_HP
        self.xp_to_next_level = config.LEVEL_UP_BASE

    def is_visible(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.fov_radius

    def heal(self, amount):
        new_hp = min(self.max_hit_points, self.get_hit_points() + amount)
        self.set_hit_points(new_hp)
        return round(amount, 2)

    def full_heal(self):
        heal_amount = self.max_hit_points - self.get_hit_points()
        self.set_hit_points(self.max_hit_points)
        return round(heal_amount, 2)

    def gain_xp(self, amount):
        self.attributes['experience'] += amount
        if self.attributes['experience'] >= self.xp_to_next_level:
            return self.level_up()
        return False

    def level_up(self):
        self.attributes['level'] += 1
        self.max_hit_points += config.HP_INCREASE_ON_LEVEL_UP
        self.attributes['power'] += config.POWER_INCREASE_ON_LEVEL_UP
        self.attributes['magic'] += config.MAGIC_INCREASE_ON_LEVEL_UP
        self.attributes['clarity'] += config.CLARITY_INCREASE_ON_LEVEL_UP
        self.xp_to_next_level = int(self.xp_to_next_level * config.LEVEL_UP_FACTOR)
        self.full_heal()
        return True

class Monster(Entity):
    def __init__(self, x, y):
        monster_type = random.choice(['Goblin', 'Orc', 'Troll', 'Skeleton'])
        char = monster_type[0].upper()
        super().__init__(x, y, char, monster_type, config.COLOR_MONSTER)
        self.adjust_attributes()

    def adjust_attributes(self):
        level_adjustment = random.randint(-2, 2)
        self.attributes['level'] += level_adjustment
        self.attributes['hit_points'] = max(1, config.MONSTER_BASE_HP + level_adjustment * 10)
        self.attributes['power'] = max(1, config.MONSTER_BASE_POWER + level_adjustment * 2)
        self.attributes['magic'] = max(1, config.MONSTER_BASE_MAGIC + level_adjustment * 2)
        self.attributes['clarity'] = max(1, config.MONSTER_BASE_CLARITY + level_adjustment * 2)
