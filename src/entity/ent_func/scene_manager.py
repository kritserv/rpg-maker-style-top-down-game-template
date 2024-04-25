from .optimizer import data_is_in_cache, add_data_to_cache, load_data_from_cache

def calculate_new_scene_data(scene_man, new_scene_name):
	scene_man.player.obs, scene_man.tdmap.rects = [], []
	for ob, color in scene_man.scene_dict[new_scene_name]:
		scene_man.player.obs.append(ob)
		scene_man.tdmap.rects.append((ob, color))
	scene_man.player.calculate_obs_pos()

def changing_scene(scene_man, x, y, new_scene_name):
	if data_is_in_cache(scene_man.cache_dict, new_scene_name):
		loaded = load_data_from_cache(scene_man.cache_dict, new_scene_name)
		scene_man.player.obs = loaded["obs_for_player"]
		scene_man.tdmap.rects = loaded["rects_for_tdmap"]
	else:
		calculate_new_scene_data(scene_man, new_scene_name)
		add_data_to_cache(scene_man.cache_dict, new_scene_name, {"obs_for_player": scene_man.player.obs, "rects_for_tdmap": scene_man.tdmap.rects})

	scene_man.player.pos = [x, y]
	scene_man.player.finish_pos = [x, y]
	scene_man.current_scene = new_scene_name

def changing_camera_stop_position(camera, stop_left, stop_right, stop_up, stop_down):
	camera.stop_follow_player_left_at_pos_x = stop_left
	camera.stop_follow_player_right_at_pos_x = stop_right
	camera.stop_follow_player_up_at_pos_y = stop_up
	camera.stop_follow_player_down_at_pos_y = stop_down