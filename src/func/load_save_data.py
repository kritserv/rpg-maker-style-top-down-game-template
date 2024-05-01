import pygame as pg
from .load_json_file import json_loader

def load_save_from_json():
	save_dict = json_loader("user_data/save.json")
	map_cam_stop_pos = json_loader("game_data/scene/camera_stop_pos.json")["camera_stop_position_dict"]

	for key in save_dict:
		if save_dict[key]:
			pos = save_dict[key]["pos"]
			scene = save_dict[key]["scene"]
			level = save_dict[key]["level"]
			items = save_dict[key]["items"]
			save_time = save_dict[key]["time"]
			img = pg.image.load(f"user_data/save_img/save_{key}.png").convert()

			effect = {
				"func": "change_scene",
				"new_scene": [pos[0], pos[1], scene], 
				"new_camera_stop_position": map_cam_stop_pos[scene],
				"img_x1": img,
				"img_x2": pg.transform.scale(img, (240, 160)),
				"img_x3": pg.transform.scale(img, (480, 320)),
				"img_x4": pg.transform.scale(img, (720, 480)),
				"level": level,
				"items": items,
				"time": save_time
			}

			save_dict[key] = effect
		else:
			save_dict[key] = {}

	return save_dict