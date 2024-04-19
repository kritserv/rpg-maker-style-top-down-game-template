import pygame as pg
import json
from src.variable import blue, white

def create_house(x, y):
	house = [
		(pg.Rect(x, y, 48, 64), blue),
		(pg.Rect(x+48, y, 16, 48), blue),
		(pg.Rect(x+64, y, 48, 64), blue)
	]
	return house

def load_scene_from_json():
	with open("game_data/scene/data.json") as f:
		json_load = json.load(f)
		loaded_scene_data = json_load["scene_data"]
		f.close()
	with open("game_data/scene/config.json") as f:
		json_load = json.load(f)
		loaded_scene_dict = json_load["scene_dict"]
		f.close()

	scene_data = {}

	if loaded_scene_data["create_house"]:
		for house in loaded_scene_data["create_house"]:
			for house_name, value in house.items():
				scene_data[house_name] = create_house(value[0], value[1])


	if loaded_scene_data["pg_rect"]:
		for rect_group in loaded_scene_data["pg_rect"]:
			for rect_group_name, rect_group_list in rect_group.items():
				for rect in rect_group_list:
					try:
						scene_data[rect_group_name].append([pg.Rect(rect), white])
					except KeyError:
						scene_data[rect_group_name] = [[pg.Rect(rect), white]]

	scene_dict = {}

	if loaded_scene_dict:
		for scene_group_name, scene_group_list in loaded_scene_dict.items():
			total_scene_group = []
			for scene_group in scene_group_list:
				total_scene_group += scene_data[scene_group]

			scene_dict[scene_group_name] = total_scene_group

	return scene_dict
