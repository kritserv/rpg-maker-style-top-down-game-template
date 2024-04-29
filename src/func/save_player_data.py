import pygame as pg
from .save_json_file import save_to_json
from .load_json_file import json_loader
from datetime import datetime


def save_player_data(player, scene_name, slot_key, screenshot):
	now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	save_dict = json_loader("user_data/save.json")
	save_dict[str(slot_key)] = {"pos": player.pos, "scene": scene_name, "time": now, "level": player.level, "items": player.items}
	try:
		pg.image.save(screenshot, f"user_data/save_img/save_{slot_key}.png")
	except TypeError:
		blank_screenshot = pg.Surface((240, 160))
		pg.image.save(blank_screenshot, f"user_data/save_img/save_{slot_key}.png")

	save_to_json("user_data/save.json", save_dict)