from json import dump

def save_to_json(path, data):
	with open(path, "w") as f:
		dump(data, f)
	f.close()