from .load_json_file import json_loader

def load_event_from_json():
	json_load = json_loader("game_data/event/config.json")
	event_dict = json_load["event_dict"]
	loaded_start_event = json_load["start_event"]

	json_load = json_loader("game_data/event/data.json")
	event_data = json_load["event_data"]

	combined_data = {}

	for key in event_dict:
		combined_data[key] = []

	for key in event_dict:
		for val in event_dict[key]:
			combined_data[key].append(event_data[val])

	start_event = event_data[loaded_start_event]

	return combined_data, start_event