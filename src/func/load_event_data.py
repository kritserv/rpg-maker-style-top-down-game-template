from json import load

def load_event_from_json():
	with open("game_data/event/config.json") as f:
		json_load = load(f)
		event_dict = json_load["event_dict"]
		loaded_start_event = json_load["start_event"]
		f.close()
	with open("game_data/event/data.json") as f:
		json_load = load(f)
		event_data = json_load["event_data"]
		f.close()

	combined_data = {}

	for key in event_dict:
		combined_data[key] = []

	for key in event_dict:
		for val in event_dict[key]:
			combined_data[key].append(event_data[val])

	start_event = event_data[loaded_start_event]

	return combined_data, start_event