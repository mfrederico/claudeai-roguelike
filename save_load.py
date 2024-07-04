import json
import os
from entities import Player
import config

SAVE_FILE = os.path.join(config.ASSETS_FOLDER, "player_save.json")

def save_game(player):
    save_data = {
        "position": {"x": player.x, "y": player.y},
        "attributes": player.attributes,
        "inventory": player.inventory,
        "armor": player.armor,
        "max_hit_points": player.max_hit_points,
        "xp_to_next_level": player.xp_to_next_level
    }
    
    with open(SAVE_FILE, 'w') as f:
        json.dump(save_data, f)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, 'r') as f:
        save_data = json.load(f)

    player = Player(save_data["position"]["x"], save_data["position"]["y"])
    player.attributes = save_data["attributes"]
    player.inventory = save_data["inventory"]
    player.armor = save_data["armor"]
    player.max_hit_points = save_data["max_hit_points"]
    player.xp_to_next_level = save_data["xp_to_next_level"]

    return player

def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
