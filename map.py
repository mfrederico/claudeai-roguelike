import random
import json
import os
import config

TERRAIN_TYPES = {
    'Rocky Terrain': {'char': '#', 'color': '\033[90m', 'passable': False, 'weight': config.TERRAIN_WEIGHTS['Rocky Terrain']},
    'Cobblestone': {'char': '.', 'color': '\033[93m', 'passable': True, 'weight': config.TERRAIN_WEIGHTS['Cobblestone']},
    'Swamp': {'char': '~', 'color': '\033[95m', 'passable': True, 'movement_cost': 2, 'weight': config.TERRAIN_WEIGHTS['Swamp']},
    'Grass': {'char': '"', 'color': '\033[92m', 'passable': True, 'weight': config.TERRAIN_WEIGHTS['Grass']},
    'Forest': {'char': '♣', 'color': '\033[32m', 'passable': True, 'fov_reduction': 2, 'weight': config.TERRAIN_WEIGHTS['Forest']},
    'Water': {'char': '≈', 'color': '\033[94m', 'passable': False, 'weight': config.TERRAIN_WEIGHTS['Water']},
    'Ocean': {'char': '▓', 'color': '\033[34m', 'passable': False, 'weight': config.TERRAIN_WEIGHTS['Ocean']},
    'Town': {'char': config.TOWN_CHAR, 'color': config.TOWN_COLOR, 'passable': True, 'weight': 0},
    'Town Entrance': {'char': config.TOWN_ENTRANCE_CHAR, 'color': config.TOWN_ENTRANCE_COLOR, 'passable': True, 'weight': 0},
}

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_file = config.MAP_FILE
        self.tiles = self.load_or_generate_map()
        self.camera_x = 0
        self.camera_y = 0

    def load_or_generate_map(self):
        if not os.path.exists(config.ASSETS_FOLDER):
            os.makedirs(config.ASSETS_FOLDER)

        if os.path.exists(self.map_file):
            return self.load_map()
        else:
            tiles = self.generate_map()
            self.save_map(tiles)
            return tiles

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

    def save_map(self, tiles):
        with open(self.map_file, 'w') as f:
            json.dump(tiles, f)

    def load_map(self):
        with open(self.map_file, 'r') as f:
            return json.load(f)

    def is_passable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return TERRAIN_TYPES[self.tiles[y][x]]['passable']
        return False

    def update_camera(self, player_x, player_y):
        self.camera_x = max(0, min(player_x - config.SCREEN_WIDTH // 2, self.width - config.SCREEN_WIDTH))
        self.camera_y = max(0, min(player_y - config.SCREEN_HEIGHT // 2, self.height - config.SCREEN_HEIGHT))

    def render(self, player, monsters, chests, towns):
        print('\033[H\033[J', end='')  # Clear screen
        self.update_camera(player.x, player.y)

        for y in range(config.SCREEN_HEIGHT):
            for x in range(config.SCREEN_WIDTH):
                map_x = x + self.camera_x
                map_y = y + self.camera_y

                if 0 <= map_x < self.width and 0 <= map_y < self.height:
                    terrain = self.tiles[map_y][map_x]
                    char = TERRAIN_TYPES[terrain]['char']
                    color = TERRAIN_TYPES[terrain]['color']

                    entity_here = None
                    for town in towns:
                        if town.x <= map_x < town.x + town.width and town.y <= map_y < town.y + town.height:
                            entity_here = ('town', town)
                            break

                    if not entity_here:
                        entity_here = next(((
                            'chest', c)
                            for c in chests
                            if c.x == map_x and c.y == map_y
                        ), None)

                    if not entity_here:
                        entity_here = next(((
                            'monster', m)
                            for m in monsters
                            if m.x == map_x and m.y == map_y
                        ), None)

                    if entity_here:
                        entity_type, entity = entity_here
                        if entity_type == 'town':
                            if (map_x, map_y) == (entity.entrance_x, entity.entrance_y):
                                char = TERRAIN_TYPES['Town Entrance']['char']
                                color = TERRAIN_TYPES['Town Entrance']['color']
                            else:
                                char = TERRAIN_TYPES['Town']['char']
                                color = TERRAIN_TYPES['Town']['color']
                        else:
                            char = entity.char
                            color = entity.color

                    if player.x == map_x and player.y == map_y:
                        char = player.char
                        color = player.color

                    if player.is_visible(map_x, map_y):
                        print(f"{color}{char}{config.COLOR_RESET}", end='')
                    else:
                        print(' ', end='')
                else:
                    print(' ', end='')
            print()

        # Render player stats
        print(f"\nPlayer: HP: {player.get_hit_points():.2f}/{player.max_hit_points} | "
              f"Power: {player.attributes['power']} | "
              f"Magic: {player.attributes['magic']} | "
              f"Clarity: {player.attributes['clarity']} | "
              f"XP: {player.attributes['experience']} | "
              f"Level: {player.attributes['level']} | "
              f"Armor: {player.armor or 'None'} | "
              f"Weapon: {player.weapon.weapon_type if player.weapon else 'None'}")
