import json
import os
from entities import Player
from items import Weapon
from town import Town
import config

PLAYER_SAVE_FILE = os.path.join(config.ASSETS_FOLDER, "player_save.json")
MAP_SAVE_FILE = os.path.join(config.ASSETS_FOLDER, "map_save.json")
TOWN_SAVE_FILE = os.path.join(config.ASSETS_FOLDER, "town_save.json")

def save_game(player, world_map, towns):
    # Save player data
    player_data = {
        "position": {"x": player.x, "y": player.y},
        "attributes": player.attributes,
        "inventory": player.inventory,
        "armor": player.armor,
        "weapon": player.weapon.weapon_type if player.weapon else None,
        "max_hit_points": player.max_hit_points,
        "xp_to_next_level": player.xp_to_next_level
    }
    with open(PLAYER_SAVE_FILE, 'w') as f:
        json.dump(player_data, f)

    # Save map data
    map_data = {
        "width": world_map.width,
        "height": world_map.height,
        "tiles": world_map.tiles
    }
    with open(MAP_SAVE_FILE, 'w') as f:
        json.dump(map_data, f)

    # Save town data
    town_data = [
        {
            "name": town.name,
            "x": town.x,
            "y": town.y,
            "entrance_x": town.entrance_x,
            "entrance_y": town.entrance_y
        }
        for town in towns
    ]
    with open(TOWN_SAVE_FILE, 'w') as f:
        json.dump(town_data, f)

def load_game():
    player = None
    world_map = None
    towns = None

    # Load player data
    if os.path.exists(PLAYER_SAVE_FILE):
        with open(PLAYER_SAVE_FILE, 'r') as f:
            player_data = json.load(f)
        player = Player(player_data["position"]["x"], player_data["position"]["y"])
        player.attributes = player_data["attributes"]
        player.inventory = player_data["inventory"]
        player.armor = player_data["armor"]
        player.max_hit_points = player_data["max_hit_points"]
        player.xp_to_next_level = player_data["xp_to_next_level"]
        if player_data["weapon"]:
            player.weapon = Weapon(player_data["weapon"])

    # Load map data
    if os.path.exists(MAP_SAVE_FILE):
        from map import GameMap  # Import here to avoid circular import
        with open(MAP_SAVE_FILE, 'r') as f:
            map_data = json.load(f)
        world_map = GameMap(map_data["width"], map_data["height"])
        world_map.tiles = map_data["tiles"]

    # Load town data
    if os.path.exists(TOWN_SAVE_FILE):
        with open(TOWN_SAVE_FILE, 'r') as f:
            town_data = json.load(f)
        towns = [
            Town(t["name"], t["x"], t["y"])
            for t in town_data
        ]
        for town, t in zip(towns, town_data):
            town.entrance_x = t["entrance_x"]
            town.entrance_y = t["entrance_y"]

    return player, world_map, towns

def delete_save():
    for file in [PLAYER_SAVE_FILE, MAP_SAVE_FILE, TOWN_SAVE_FILE]:
        if os.path.exists(file):
            os.remove(file)
