import pygame as pg
from src import blit_text
from src.variable import screen, white, black, debug_font
from .ent_func import data_is_in_cache, add_data_to_cache, load_data_from_cache

class Debugger:
	def __init__(self):
		self.cache_dict = {}

	def print_debug(self, print_list):
		key = str(len(print_list))
		if data_is_in_cache(self.cache_dict, key):
			debug_background = load_data_from_cache(self.cache_dict, key)
		else:
			debug_background = pg.Surface((300, len(print_list) * 22))
			debug_background.set_alpha(150)
			debug_background.fill(black)
			debug_background = debug_background.convert_alpha()
			add_data_to_cache(self.cache_dict, key, debug_background)
			
		screen.blit(debug_background, (0, 0))
		y_pos = 5
		for text in print_list:
			if not isinstance(text, str):
				text = str(text)
			blit_text(text, debug_font, white, (5, y_pos))
			y_pos += 20
