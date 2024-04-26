from .load_json_file import json_loader

def load_event_from_json():
	json_load = json_loader("game_data/event/config.json")
	event_dict = json_load["event_dict"]
	loaded_start_event = json_load["start_event"]

	json_load = json_loader("game_data/event/data.json")
	event_data = json_load["event_data"]

	json_load = json_loader("game_data/scene/camera_stop_pos.json")
	camera_stop_pos_data = json_load["camera_stop_position_dict"]

	combined_data = {}

	for key in event_dict:
		combined_data[key] = []

	for key in event_dict:
		for val in event_dict[key]:
			map_name = event_data[val]["effect"]["new_scene"][2]
			map_cam_stop_pos = camera_stop_pos_data[map_name]
			event_data[val]["effect"]["new_camera_stop_position"] = map_cam_stop_pos
			combined_data[key].append(event_data[val])

	start_event = event_data[loaded_start_event]
	map_name = start_event["effect"]["new_scene"][2]
	map_cam_stop_pos = camera_stop_pos_data[map_name]
	start_event["effect"]["new_camera_stop_position"] = map_cam_stop_pos

	return combined_data, start_event