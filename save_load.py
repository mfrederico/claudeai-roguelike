import json
import os
from entities import Player
from items import Weapon
from town import Town
import config

SAVE_FILE = os.path.join(config.ASSETS_FOLDER, "game_save.json")

def save_game(player, towns):
    save_data = {
        "player": {
            "position": {"x": player.x, "y": player.y},
            "attributes": player.attributes,
            "inventory": player.inventory,
            "armor": player.armor,
            "weapon": player.weapon.weapon_type if player.weapon else None,
            "max_hit_points": player.max_hit_points,
            "xp_to_next_level": player.xp_to_next_level
        },
        "towns": [
            {
                "name": town.name,
                "x": town.x,
                "y": town.y,
                "entrance_x": town.entrance_x,
                "entrance_y": town.entrance_y
            }
            for town in towns
        ]
    }
    
    with open(SAVE_FILE, 'w') as f:
        json.dump(save_data, f)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None, None

    with open(SAVE_FILE, 'r') as f:
        save_data = json.load(f)

    player_data = save_data["player"]
    player = Player(player_data["position"]["x"], player_data["position"]["y"])
    player.attributes = player_data["attributes"]
    player.inventory = player_data["inventory"]
    player.armor = player_data["armor"]
    player.max_hit_points = player_data["max_hit_points"]
    player.xp_to_next_level = player_data["xp_to_next_level"]

    if player_data["weapon"]:
        player.weapon = Weapon(player_data["weapon"])
    else:
        player.weapon = None

    towns = [
        Town(t["name"], t["x"], t["y"])
        for t in save_data["towns"]
    ]
    for town, town_data in zip(towns, save_data["towns"]):
        town.entrance_x = town_data["entrance_x"]
        town.entrance_y = town_data["entrance_y"]

    return player, towns

def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

