import os

# Asset paths
ASSETS_FOLDER = "assets"
MAP_FILE = os.path.join(ASSETS_FOLDER, "game_map.json")

# Map configuration
MAP_WIDTH = 160
MAP_HEIGHT = 90
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24

# Game mechanics
NUM_MONSTERS = 50
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

# Field of View
PLAYER_FOV_RADIUS = 5

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

# Color codes
COLOR_RESET = '\033[0m'
COLOR_PLAYER = '\033[1;33m'
COLOR_MONSTER = '\033[1;31m'
