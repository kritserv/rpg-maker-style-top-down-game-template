from .save_json_file import save_to_json
from .load_json_file import json_loader

def save_player_data(player, scene_name, slot_key):
	save_dict = json_loader("user_data/save.json")
	save_dict[str(slot_key)] = {"pos": player.pos, "scene": scene_name}

	save_to_json("user_data/save.json", save_dict)