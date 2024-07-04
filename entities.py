import math

class Entity:
    def __init__(self, x, y, char, name, color='\033[0m'):
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
            'power': 20,
            'magic': 20,
            'clarity': 20,
            'hit_points': 100,
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

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '@', 'Player', '\033[1;33m')
        self.fov_radius = 5

    def is_visible(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.fov_radius

class Monster(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'M', 'Monster', '\033[1;31m')
