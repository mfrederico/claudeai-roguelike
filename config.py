import os

# Color codes
COLOR_RESET = '\033[0m'
COLOR_PLAYER = '\033[1;33m'
COLOR_MONSTER = '\033[1;31m'


# Chest configuration
CHEST_CHAR = '▣'
CHEST_COLOR = '\033[1;33m'  # Bright yellow
NUM_CHESTS = 100  # Number of chests to spawn on the map

# Treasure probabilities
TREASURE_TYPES = {
    'armor': 0.5,  # 50% chance of armor
    'weapon': 0.5  # 50% chance of weapon
}

# Town generation
TOWN_SIZE = 8  # Fixed size for all towns
NUM_TOWNS = 30
TOWN_CHAR = '▣'
TOWN_COLOR = '\033[1;36m'  # Cyan
TOWN_ENTRANCE_CHAR = '▼'
TOWN_ENTRANCE_COLOR = '\033[1;33m'  # Yellow

# Asset paths
ASSETS_FOLDER = "assets"
MAP_FILE = os.path.join(ASSETS_FOLDER, "game_map.json")

# Map configuration
MAP_WIDTH = 160
MAP_HEIGHT = 90
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24

# Game mechanics
NUM_MONSTERS = 150
MONSTER_MOVE_CHANCE = 0.5  # 50% chance for a monster to move each turn

# Monster spawning
REGION_DIVISIONS_X = 5
REGION_DIVISIONS_Y = 5
MAX_SPAWN_ATTEMPTS = 100

# Combat
PLAYER_STARTING_HP = 100
MONSTER_BASE_HP = 50
PLAYER_STARTING_POWER = 20
MONSTER_BASE_POWER = 15
PLAYER_STARTING_MAGIC = 20
MONSTER_BASE_MAGIC = 10
PLAYER_STARTING_CLARITY = 20
MONSTER_BASE_CLARITY = 10


# Experience and leveling
XP_GAIN_MULTIPLIER = 10
LEVEL_UP_BASE = 100
LEVEL_UP_FACTOR = 1.5

# Leveling up
LEVEL_UP_BASE = 100
LEVEL_UP_FACTOR = 1.5
HP_INCREASE_ON_LEVEL_UP = 20
POWER_INCREASE_ON_LEVEL_UP = 1
MAGIC_INCREASE_ON_LEVEL_UP = 1
CLARITY_INCREASE_ON_LEVEL_UP = 1

# Field of View
PLAYER_FOV_RADIUS = 100

# Terrain types
TERRAIN_TYPES = {
    'Rocky Terrain': {'char': '#', 'color': '\033[90m', 'passable': False, 'weight': 5},
    'Cobblestone': {'char': '·', 'color': '\033[1;33m', 'passable': True, 'weight': 20},  # Bright yellow
    'Swamp': {'char': '~', 'color': '\033[95m', 'passable': True, 'movement_cost': 2, 'weight': 10},
    'Grass': {'char': '"', 'color': '\033[92m', 'passable': True, 'weight': 40},
    'Forest': {'char': '♣', 'color': '\033[32m', 'passable': True, 'fov_reduction': 2, 'weight': 20},
    'Water': {'char': '≈', 'color': '\033[94m', 'passable': False, 'weight': 5},
    'Ocean': {'char': '▓', 'color': '\033[34m', 'passable': False, 'weight': 0},
}

# Terrain generation weights
TERRAIN_WEIGHTS = {
    'Rocky Terrain': 5,
    'Cobblestone': 20,
    'Swamp': 10,
    'Grass': 40,
    'Forest': 20,
    'Water': 5,
    'Ocean': 0  # Ocean is only used for borders
}

# Weapon types and their attack bonuses
WEAPON_TYPES = {
    'Dagger': 0.10,
    'Club': 0.20,
    'Sword': 0.35,
    'Axe': 0.40,
    'Mace': 0.55,
    'Twig': 'instant'  # Special case for instant death
}

# Armor types and their protection values
ARMOR_TYPES = {
    'Cloth': 0.10,
    'Leather': 0.20,
    'Scale': 0.30,
    'Chain': 0.50,
    'Plate': 0.80,
    'Carbon-Fiber': 1.00
}
