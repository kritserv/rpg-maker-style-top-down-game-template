import pygame as pg
import json
from variable import blue, white

def create_house(x, y):
	house = [
		(pg.Rect(x, y, 48, 64), blue),
		(pg.Rect(x+48, y, 16, 48), blue),
		(pg.Rect(x+64, y, 48, 64), blue)
	]
	return house

def load_scene_from_json():
	with open("data/scene.json") as f:
		json_load = json.load(f)
		scene_data = json_load["scene_data"]
		f.close()

	loaded_scene_data = {}

	if scene_data["create_house"]:
		for house in scene_data["create_house"]:
			for house_name, value in house.items():
				loaded_scene_data[house_name] = create_house(value[0], value[1])


	if scene_data["pg_rect"]:
		for rect_group in scene_data["pg_rect"]:
			for rect_group_name, rect_group_list in rect_group.items():
				for rect in rect_group_list:
					try:
						loaded_scene_data[rect_group_name].append([pg.Rect(rect), white])
					except KeyError:
						loaded_scene_data[rect_group_name] = [[pg.Rect(rect), white]]

	return loaded_scene_data