import pygame as pg
from src.variable import black
from .ent_func import data_is_in_cache, add_data_to_cache, load_data_from_cache

class BlackBar:
	def __init__(self, screen, is_exist):
		self.screen = screen
		self.is_exist = is_exist
		self.cache_dict = {}

	def calculate_new_resolution(self, curr_width, curr_height, ratio):
		need_to_draw = curr_width / curr_height > ratio
		black_bar_width = (curr_width - curr_height * ratio) / 2
		return need_to_draw, black_bar_width

	def draw_if_set(self, curr_width, curr_height, ratio):
		if self.is_exist:
			data_key = str(curr_width)+str(curr_height)
			if data_is_in_cache(self.cache_dict, data_key):
				need_to_draw, self.black_bar_width = load_data_from_cache(self.cache_dict, data_key)
			else:
				need_to_draw, self.black_bar_width = self.calculate_new_resolution(curr_width, curr_height, ratio)
				add_data_to_cache(self.cache_dict, data_key, [need_to_draw, self.black_bar_width])

			if need_to_draw:
				self.draw_black_bar(curr_width, curr_height)

	def draw_black_bar(self, curr_width, curr_height):
		pg.draw.rect(self.screen, black, (0, 0, self.black_bar_width, curr_height))
		pg.draw.rect(self.screen, black, (curr_width - self.black_bar_width, 0, self.black_bar_width + 1, curr_height))
