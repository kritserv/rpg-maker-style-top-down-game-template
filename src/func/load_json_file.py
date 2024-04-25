from json import load

def json_loader(path):
	with open(path) as f:
		json_load = load(f)
		f.close()
		return json_load