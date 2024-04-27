import pygame as pg
from src import blit_text
from src.variable import screen, white, black, debug_font
from .ent_func import data_is_in_cache, add_data_to_cache, load_data_from_cache

class Debugger:
	def __init__(self):
		self.background_cache_dict = {}
		self.black_bar_cache_dict = {}

	def print_debug(self, print_list, black_bar):
		key = str(len(print_list))
		if data_is_in_cache(self.background_cache_dict, key):
			debug_background = load_data_from_cache(self.background_cache_dict, key)
		else:
			debug_background = pg.Surface((300, len(print_list) * 22))
			debug_background.set_alpha(150)
			debug_background.fill(black)
			debug_background = debug_background.convert_alpha()
			add_data_to_cache(self.background_cache_dict, key, debug_background)

		top_left_x = 0
		if black_bar.is_exist:
			key = str(black_bar.black_bar_width)
			if data_is_in_cache(self.black_bar_cache_dict, key):
				top_left_x = load_data_from_cache(self.black_bar_cache_dict, key)
			else:
				if black_bar.black_bar_width > 0:
					top_left_x = black_bar.black_bar_width
				add_data_to_cache(self.black_bar_cache_dict, key, top_left_x)
				
		screen.blit(debug_background, (top_left_x, 0))
		top_left_y = 5
		for text in print_list:
			if not isinstance(text, str):
				text = str(text)
			blit_text(text, debug_font, white, (top_left_x + 5, top_left_y))
			top_left_y += 20
