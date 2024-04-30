import pygame as pg
from .load_json_file import json_loader

def load_img_and_pos(img_and_pos):
	img_name = img_and_pos["img"]

	img_path = f"asset/img/scene/{img_name}"

	img_x1 = pg.image.load(img_path).convert()
	img_width, img_height = img_x1.get_size()
	img_x2 = pg.transform.scale(img_x1, (img_width*2, img_height*2)).convert()
	img_x3 = pg.transform.scale(img_x1, (img_width*3, img_height*3)).convert()

	pos = img_and_pos["pos"]

	return img_x1, img_x2, img_x3, pos


def load_asset_from_json():
	json_load = json_loader("game_data/scene/render.json")["render_dict"]

	scene_render_dict = {}

	for scene_name in json_load:
		layer = json_load[scene_name]

		behind_player = []
		in_front_of_player = []

		if layer["behind_player"]:
			for img_and_pos in layer["behind_player"]:

				img_x1, img_x2, img_x3, pos = load_img_and_pos(img_and_pos)

				behind_player.append([img_x1, img_x2, img_x3, pos])

		if layer["in_front_of_player"]:
			for img_and_pos in layer["in_front_of_player"]:

				img_x1, img_x2, img_x3, pos = load_img_and_pos(img_and_pos)

				in_front_of_player.append([img_x1, img_x2, img_x3, pos])

		scene_render_dict[scene_name] = {"behind_player": behind_player, "in_front_of_player": in_front_of_player}

	return scene_render_dict
