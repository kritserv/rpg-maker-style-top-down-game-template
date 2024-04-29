import pygame as pg
from src import font_x1, font_x1_5, font_x2, font_x2_5, font_x3, font_x3_5, font_x4, blit_text
from src.variable import white, black
from .ent_func import data_is_in_cache, add_data_to_cache, load_data_from_cache

class TextBox:
	def __init__(self, screen):
		self.screen = screen
		self.top_left_x, self.top_left_y = 8, 8
		self.original_top_left_x = 8

		self.background_cache_dict = {}
		self.black_bar_cache_dict = {}

	def reset_cache(self):
		self.top_left_x = 8
		self.background_cache_dict = {}
		self.black_bar_cache_dict = {}

	def draw_background_with_black_bar(self, pixel_size, black_bar_width):
		key = str(self.screen.get_width())+str(self.screen.get_height())+str(black_bar_width)+str(pixel_size)
		if data_is_in_cache(self.background_cache_dict, key):
			self.text_box_background = load_data_from_cache(self.background_cache_dict, key)
		else:
			self.text_box_background = pg.Surface((self.screen.get_width() - (black_bar_width*2) - 16, self.screen.get_height()/4))
			self.text_box_background.set_alpha(200)
			self.text_box_background.fill(black)
			self.text_box_background = self.text_box_background.convert_alpha()
			add_data_to_cache(self.background_cache_dict, key, self.text_box_background)
		self.screen.blit(self.text_box_background, (self.top_left_x, self.top_left_y))

	def draw_background(self, pixel_size):
		key = str(self.screen.get_width())+str(self.screen.get_height())
		if data_is_in_cache(self.background_cache_dict, key):
			self.text_box_background = load_data_from_cache(self.background_cache_dict, key)
		else:
			self.text_box_background = pg.Surface((self.screen.get_width()-16, self.screen.get_height()/4))
			self.text_box_background.set_alpha(200)
			self.text_box_background.fill(black)
			self.text_box_background = self.text_box_background.convert_alpha()
			add_data_to_cache(self.background_cache_dict, key, self.text_box_background)
		self.screen.blit(self.text_box_background, (self.top_left_x, self.top_left_y))

	def draw(self, pixel_size, black_bar, text):

		if black_bar.is_exist:
			key = str(black_bar.black_bar_width)
			if data_is_in_cache(self.black_bar_cache_dict, key):
				self.top_left_x = load_data_from_cache(self.black_bar_cache_dict, key)
			else:
				if black_bar.black_bar_width > 0:
					self.top_left_x = self.original_top_left_x + black_bar.black_bar_width
				else:
					self.top_left_x = self.original_top_left_x
				add_data_to_cache(self.black_bar_cache_dict, key, self.top_left_x)

			self.draw_background_with_black_bar(pixel_size, black_bar.black_bar_width)

		else:
			self.draw_background(pixel_size)

		pixel_size += 1.5

		if pixel_size == 1:
			text_font = font_x1
		elif pixel_size == 1.5:
			text_font = font_x1_5
		elif pixel_size == 2:
			text_font = font_x2
		elif pixel_size == 2.5:
			text_font = font_x2_5
		elif pixel_size == 3:
			text_font = font_x3
		elif pixel_size == 3.5:
			text_font = font_x3_5
		else:
			text_font = font_x4

		if "\n" in text:
			lines = text.split("\n")
			y = self.top_left_y + 8
			range_y = 8
			for line in lines:
				blit_text(line, text_font, white, [self.top_left_x + 4 * pixel_size, y])
				y += (range_y * pixel_size)
		else:
			blit_text(text, text_font, white, [self.top_left_x + 4 * pixel_size, self.top_left_y + 8])