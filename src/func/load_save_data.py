from .load_json_file import json_loader

def load_save_from_json():
	save_dict = json_loader("user_data/save.json")

	return save_dict
