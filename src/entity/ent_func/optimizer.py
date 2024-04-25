def data_is_in_cache(cache_dict, data_key):
	try:
		test = cache_dict[data_key]
		return True
	except KeyError:
		return False

def add_data_to_cache(cache_dict, data_key, data):
	cache_dict[data_key] = data

def load_data_from_cache(cache_dict, data_key):
	return cache_dict[data_key]