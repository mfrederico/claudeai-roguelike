import random

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24

TERRAIN_TYPES = {
    'Rocky Terrain': {'char': '#', 'color': '\033[90m', 'passable': False, 'weight': 5},
    'Cobblestone': {'char': '.', 'color': '\033[93m', 'passable': True, 'weight': 20},
    'Swamp': {'char': '~', 'color': '\033[95m', 'passable': True, 'movement_cost': 2, 'weight': 10},
    'Grass': {'char': '"', 'color': '\033[92m', 'passable': True, 'weight': 40},
    'Forest': {'char': '♣', 'color': '\033[32m', 'passable': True, 'fov_reduction': 2, 'weight': 20},
    'Water': {'char': '≈', 'color': '\033[94m', 'passable': False, 'weight': 5},
    'Ocean': {'char': '▓', 'color': '\033[34m', 'passable': False, 'weight': 0},
}

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.generate_map()
        self.camera_x = 0
        self.camera_y = 0

    def generate_map(self):
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    row.append('Ocean')
                else:
                    terrain = random.choices(
                        list(TERRAIN_TYPES.keys()),
                        weights=[t['weight'] for t in TERRAIN_TYPES.values()]
                    )[0]
                    row.append(terrain)
            tiles.append(row)
        return tiles

    def is_passable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return TERRAIN_TYPES[self.tiles[y][x]]['passable']
        return False

    def update_camera(self, player_x, player_y):
        self.camera_x = max(0, min(player_x - SCREEN_WIDTH // 2, self.width - SCREEN_WIDTH))
        self.camera_y = max(0, min(player_y - SCREEN_HEIGHT // 2, self.height - SCREEN_HEIGHT))

    def render(self, player, monsters):
        print('\033[H\033[J', end='')  # Clear screen
        self.update_camera(player.x, player.y)

        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                map_x = x + self.camera_x
                map_y = y + self.camera_y
                
                if 0 <= map_x < self.width and 0 <= map_y < self.height:
                    terrain = self.tiles[map_y][map_x]
                    char = TERRAIN_TYPES[terrain]['char']
                    color = TERRAIN_TYPES[terrain]['color']
                    
                    monster_here = next((m for m in monsters if m.x == map_x and m.y == map_y), None)
                    if monster_here:
                        char = monster_here.char
                        color = monster_here.color

                    if player.x == map_x and player.y == map_y:
                        char = player.char
                        color = player.color

                    if player.is_visible(map_x, map_y):
                        print(f"{color}{char}\033[0m", end='')
                    else:
                        print(' ', end='')
                else:
                    print(' ', end='')
            print()

        print(f"\nPlayer: HP: {player.attributes['hit_points']} | "
              f"Power: {player.attributes['power']} | "
              f"Magic: {player.attributes['magic']} | "
              f"Clarity: {player.attributes['clarity']} | "
              f"XP: {player.attributes['experience']} | "
              f"Level: {player.attributes['level']}")

        print("\nUse WASD to move, Q to quit")
