import pygame as pg
from variable.settings import black

class BlackBar:
	def __init__(self, screen, is_exist):
		self.screen = screen
		self.black_bar_width = 0
		self.is_exist = is_exist

	def draw_if_set(self, curr_width, curr_height, ratio):
		if self.is_exist:
			need_to_draw_bar = curr_width / curr_height > ratio
			if need_to_draw_bar:
				self.black_bar_width = (curr_width - curr_height * ratio) / 2
				self.draw_black_bar(curr_width, curr_height)

	def draw_black_bar(self, curr_width, curr_height):
		pg.draw.rect(self.screen, black, (0, 0, self.black_bar_width, curr_height))
		pg.draw.rect(self.screen, black, (curr_width - self.black_bar_width, 0, self.black_bar_width + 1, curr_height))
