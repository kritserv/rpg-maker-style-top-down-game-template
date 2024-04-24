import pygame as pg
from src.variable import black

class BlackBar:
	def __init__(self, screen, is_exist):
		self.screen = screen
		self.is_exist = is_exist
		self.cache_dict = {}

	def resolution_is_in_cache(self, curr_width, curr_height):
		try:
			test = self.cache_dict[str(curr_width)+str(curr_height)]
			return True
		except KeyError:
			return False

	def add_resolution_to_cache(self, curr_width, curr_height, data):
		self.cache_dict[str(curr_width)+str(curr_height)] = data

	def load_resolution_from_cache(self, curr_width, curr_height):
		return self.cache_dict[str(curr_width)+str(curr_height)]

	def calculate_new_resolution(self, curr_width, curr_height, ratio):
		need_to_draw = curr_width / curr_height > ratio
		black_bar_width = (curr_width - curr_height * ratio) / 2
		return need_to_draw, black_bar_width

	def draw_if_set(self, curr_width, curr_height, ratio):
		if self.is_exist:
			if self.resolution_is_in_cache(curr_width, curr_height):
				need_to_draw, self.black_bar_width = self.load_resolution_from_cache(curr_width, curr_height)
			else:
				need_to_draw, self.black_bar_width = self.calculate_new_resolution(curr_width, curr_height, ratio)
				self.add_resolution_to_cache(curr_width, curr_height, [need_to_draw, self.black_bar_width])

			if need_to_draw:
				self.draw_black_bar(curr_width, curr_height)

	def draw_black_bar(self, curr_width, curr_height):
		pg.draw.rect(self.screen, black, (0, 0, self.black_bar_width, curr_height))
		pg.draw.rect(self.screen, black, (curr_width - self.black_bar_width, 0, self.black_bar_width + 1, curr_height))
