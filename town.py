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
        
        if is_suitable_town_location(world_map, x, y, towns):
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
        print(f"Town: {town.name} at ({town.x}, {town.y}), entrance at ({town.entrance_x}, {town.entrance_y})")
    
    return towns

def is_suitable_town_location(world_map, x, y, existing_towns):
    # Check if the town fits within the map boundaries
    if not (0 <= x < world_map.width - config.TOWN_SIZE and
            0 <= y < world_map.height - config.TOWN_SIZE):
        return False

    # Check for overlap with existing towns
    for town in existing_towns:
        if (x < town.x + town.width and x + config.TOWN_SIZE > town.x and
            y < town.y + town.height and y + config.TOWN_SIZE > town.y):
            return False

    # Check if the area is not in water
    for i in range(x, x + config.TOWN_SIZE):
        for j in range(y, y + config.TOWN_SIZE):
            if world_map.tiles[j][i] in ['Water', 'Ocean']:
                return False

    return True

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
    
    # Determine which direction to go first (horizontal or vertical)
    if random.choice([True, False]):
        # Horizontal first, then vertical
        generate_path_segment(world_map, x1, y1, x2, y1)
        generate_path_segment(world_map, x2, y1, x2, y2)
    else:
        # Vertical first, then horizontal
        generate_path_segment(world_map, x1, y1, x1, y2)
        generate_path_segment(world_map, x1, y2, x2, y2)

def generate_path_segment(world_map, x1, y1, x2, y2):
    dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
    dy = 1 if y2 > y1 else -1 if y2 < y1 else 0
    
    current_x, current_y = x1, y1
    while current_x != x2 or current_y != y2:
        if 0 <= current_x < world_map.width and 0 <= current_y < world_map.height:
            if world_map.tiles[current_y][current_x] not in ['Rocky Terrain', 'Town Entrance', 'Ocean', 'Water']:
                world_map.tiles[current_y][current_x] = 'Cobblestone'
        
        if current_x != x2:
            current_x += dx
        elif current_y != y2:
            current_y += dy

