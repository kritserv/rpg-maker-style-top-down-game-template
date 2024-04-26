def data_is_in_cache(cache_dict, data_key):
	try:
		test = cache_dict[data_key]
		return True
	except KeyError:
		return False

def clear_cache(cache_dict):
	cache_dict = {}

def add_data_to_cache(cache_dict, data_key, data):
	
	if len(cache_dict) >= 20:
		clear_cache(cache_dict)

	cache_dict[data_key] = data

def load_data_from_cache(cache_dict, data_key):
	return cache_dict[data_key]