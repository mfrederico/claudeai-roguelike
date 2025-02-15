import random
import json
import os
import noise
import config

TERRAIN_TYPES = {
    'Rocky Terrain': {'char': '#', 'color': '\033[90m', 'passable': False},
    'Cobblestone': {'char': '·', 'color': '\033[1;33m', 'passable': True},
    'Swamp': {'char': '~', 'color': '\033[95m', 'passable': True, 'movement_cost': 2},
    'Grass': {'char': '"', 'color': '\033[92m', 'passable': True},
    'Forest': {'char': '♣', 'color': '\033[32m', 'passable': True, 'fov_reduction': 2},
    'Water': {'char': '≈', 'color': '\033[94m', 'passable': False},
    'Ocean': {'char': '▓', 'color': '\033[34m', 'passable': False},
    'Town': {'char': config.TOWN_CHAR, 'color': config.TOWN_COLOR, 'passable': True},
    'Town Entrance': {'char': config.TOWN_ENTRANCE_CHAR, 'color': config.TOWN_ENTRANCE_COLOR, 'passable': True},
}

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.generate_map()
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
        # Adjust scales based on map size
        base_scale = min(self.width, self.height) / 100  # Base scale factor
        elevation_scale = base_scale * 2
        moisture_scale = base_scale * 2
        rivers_scale = base_scale * 4
        lakes_scale = base_scale * 3

        octaves = min(6, max(2, int(base_scale * 3)))  # Adjust octaves based on map size
        persistence = 0.5
        lacunarity = 2.0
        seed = random.randint(0, 100000)

        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                nx = x / self.width
                ny = y / self.height

                elevation = noise.pnoise2(nx * elevation_scale,
                                          ny * elevation_scale,
                                          octaves=octaves,
                                          persistence=persistence,
                                          lacunarity=lacunarity,
                                          repeatx=1,
                                          repeaty=1,
                                          base=seed)
                
                moisture = noise.pnoise2(nx * moisture_scale + 5.2,
                                         ny * moisture_scale + 1.3,
                                         octaves=octaves,
                                         persistence=persistence,
                                         lacunarity=lacunarity,
                                         repeatx=1,
                                         repeaty=1,
                                         base=seed + 1)

                rivers = noise.pnoise2(nx * rivers_scale + 10.5,
                                       ny * rivers_scale + 3.7,
                                       octaves=max(2, octaves - 2),
                                       persistence=persistence,
                                       lacunarity=lacunarity,
                                       repeatx=1,
                                       repeaty=1,
                                       base=seed + 2)

                lakes = noise.pnoise2(nx * lakes_scale + 15.7,
                                      ny * lakes_scale + 8.3,
                                      octaves=max(2, octaves - 1),
                                      persistence=persistence,
                                      lacunarity=lacunarity,
                                      repeatx=1,
                                      repeaty=1,
                                      base=seed + 3)

                terrain = self.get_terrain_type(elevation, moisture, rivers, lakes)
                row.append(terrain)
            tiles.append(row)

        return tiles

    def get_terrain_type(self, elevation, moisture, rivers, lakes):
        if elevation < -0.3:
            return 'Ocean'
        elif rivers > 0.2 or lakes > 0.3:
            return 'Water'
        elif elevation < -0.1:
            if moisture > 0:
                return 'Swamp'
            else:
                return 'Grass'
        elif elevation < 0.2:
            if moisture < -0.2:
                return 'Grass'
            elif moisture < 0.2:
                return 'Forest'
            else:
                return 'Swamp'
        elif elevation < 0.5:
            if moisture < 0:
                return 'Grass'
            else:
                return 'Forest'
        else:
            return 'Rocky Terrain'

    def is_passable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return TERRAIN_TYPES[self.tiles[y][x]]['passable']
        return False


    def save_map(self, tiles):
        with open(self.map_file, 'w') as f:
            json.dump(tiles, f)

    def load_map(self):
        with open(self.map_file, 'r') as f:
            return json.load(f)

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
