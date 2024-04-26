from .load_json_file import json_loader

def load_save_from_json():
	save_dict = {}
	json_load = json_loader("user_data/save.json")
	event_data_json_load = json_loader("game_data/event/data.json")["event_data"]

	for key in json_load:
		if json_load[key]:
			pos = json_load[key]["pos"]
			scene = json_load[key]["scene"]
			event_name = f"move_to_{scene}" 
			event = event_data_json_load[event_name]["effect"]
			event["new_scene"] = [pos[0], pos[1], scene]
			sub_dict = {
				"event": event
			}

			save_dict[key] = sub_dict
		else:
			save_dict[key] = {}

	return save_dict