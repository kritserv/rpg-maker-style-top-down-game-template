from .load_json_file import json_loader

def load_save_from_json():
	save_dict = json_loader("user_data/save.json")
	map_cam_stop_pos = json_loader("game_data/scene/camera_stop_pos.json")["camera_stop_position_dict"]

	for key in save_dict:
		if save_dict[key]:
			pos = save_dict[key]["pos"]
			scene = save_dict[key]["scene"]

			effect = {
				"func": "change_scene",
				"new_scene": [pos[0], pos[1], scene], 
				"new_camera_stop_position": map_cam_stop_pos[scene]
			}

			save_dict[key] = effect
		else:
			save_dict[key] = {}

	return save_dict