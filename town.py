import random
import config

class Town:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.width = config.TOWN_SIZE
        self.height = config.TOWN_SIZE
        self.entrance_x = None
        self.entrance_y = None

def generate_towns(world_map):
    towns = []
    attempts = 0
    max_attempts = 1000

    while len(towns) < config.NUM_TOWNS and attempts < max_attempts:
        name = f"Town-{random.randint(1, 1000)}"
        x = random.randint(0, world_map.width - config.TOWN_SIZE)
        y = random.randint(0, world_map.height - config.TOWN_SIZE)
        
        if is_suitable_town_location(world_map, x, y):
            town = Town(name, x, y)
            place_town_on_map(world_map, town)
            towns.append(town)
        
        attempts += 1
    
    # Generate paths between towns
    if len(towns) > 1:
        for i in range(len(towns) - 1):
            generate_path(world_map, towns[i], towns[i + 1])
    
    print(f"Generated {len(towns)} towns")
    for town in towns:
        print(f"Town: {town.name} at ({town.x}, {town.y})")
    
    return towns

def is_suitable_town_location(world_map, x, y):
    # Check if the town fits within the map boundaries
    return (0 <= x < world_map.width - config.TOWN_SIZE and
            0 <= y < world_map.height - config.TOWN_SIZE)

def place_town_on_map(world_map, town):
    for i in range(town.width):
        for j in range(town.height):
            if i == 0 or i == town.width - 1 or j == 0 or j == town.height - 1:
                world_map.tiles[town.y + j][town.x + i] = 'Rocky Terrain'
            else:
                world_map.tiles[town.y + j][town.x + i] = 'Cobblestone'
    
    # Place town entrance
    entrance_sides = [(0, town.height // 2), (town.width - 1, town.height // 2),
                      (town.width // 2, 0), (town.width // 2, town.height - 1)]
    entrance = random.choice(entrance_sides)
    town.entrance_x = town.x + entrance[0]
    town.entrance_y = town.y + entrance[1]
    world_map.tiles[town.entrance_y][town.entrance_x] = 'Town Entrance'

def generate_path(world_map, town1, town2):
    x1, y1 = town1.entrance_x, town1.entrance_y
    x2, y2 = town2.entrance_x, town2.entrance_y
    
    # Use a simple line drawing algorithm to create the path
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while x1 != x2 or y1 != y2:
        if 0 <= x1 < world_map.width and 0 <= y1 < world_map.height:
            if world_map.tiles[y1][x1] not in ['Rocky Terrain', 'Town Entrance', 'Ocean']:
                world_map.tiles[y1][x1] = 'Cobblestone'
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

