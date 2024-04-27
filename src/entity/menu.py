import pygame as pg
from src import font_x1, font_x2, font_x3, font_x4, blit_text
from src.variable import green, black
from .ent_func import data_is_in_cache, add_data_to_cache, load_data_from_cache

class Menu:
	def __init__(self, cursor):
		self.cursor = cursor
		self.buttons = []
		self.button_dicts = {}
		self.plus_value = 10
		self.columns = 1
		self.top_left_x, self.top_left_y = 8, 8
		self.original_top_left_x = 8
		self.font_size_plus_1 = False

		self.background_cache_dict = {}
		self.black_bar_cache_dict = {}

		self.need_background = True

	def calculate_menu_obs_pos(self):
		self.top = -32
		top = [-16, self.top, 16*self.columns, 16]
		self.bottom = (len(self.buttons) - 1) * 16
		bottom = [-16, self.bottom, 16*self.columns, 16]
		left = [-32, self.top, 16, self.bottom + 48]
		right = [16*(self.columns-1), self.top, 16, self.bottom + 48]
		self.cursor.obs = [top, bottom, left, right]
		self.cursor.calculate_obs_pos()

	def calculate_button_pos(self):
		for i in range(len(self.buttons)):
			button_pos = i*16
			self.button_dicts[button_pos] = self.buttons[i]

	def setup_buttons(self):
		self.calculate_menu_obs_pos()
		self.calculate_button_pos()

	def reset_cursor(self):
		self.cursor.pos[1] = 0

	def draw_background_with_black_bar(self, pixel_size, black_bar_width):
		screen = self.cursor.screen
		key = str(self.cursor.original_width)+str(black_bar_width)+str(pixel_size)
		if data_is_in_cache(self.background_cache_dict, key):
			self.menu_background = load_data_from_cache(self.background_cache_dict, key)
		else:
			self.menu_background = pg.Surface((self.cursor.original_width * pixel_size * self.columns, 16 * pixel_size * len(self.buttons)))
			self.menu_background.set_alpha(200)
			self.menu_background.fill(black)
			self.menu_background = self.menu_background.convert_alpha()
			add_data_to_cache(self.background_cache_dict, key, self.menu_background)
		screen.blit(self.menu_background, (self.top_left_x, self.top_left_y))

	def draw_background(self, pixel_size):
		screen = self.cursor.screen
		key = str(self.cursor.original_width)+str(pixel_size)
		if data_is_in_cache(self.background_cache_dict, key):
			self.menu_background = load_data_from_cache(self.background_cache_dict, key)
		else:
			self.menu_background = pg.Surface((self.cursor.original_width * pixel_size * self.columns, 16 * pixel_size * len(self.buttons)))
			self.menu_background.set_alpha(200)
			self.menu_background.fill(black)
			self.menu_background = self.menu_background.convert_alpha()
			add_data_to_cache(self.background_cache_dict, key, self.menu_background)
		screen.blit(self.menu_background, (self.top_left_x, self.top_left_y))

	def draw(self, pixel_size, black_bar):

		if self.font_size_plus_1:
			pixel_size += 1

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

		if self.need_background:
			if black_bar.is_exist:
				self.draw_background_with_black_bar(pixel_size, black_bar.black_bar_width)
			else:
				self.draw_background(pixel_size)

		self.cursor.draw(pixel_size, self.top_left_x, self.top_left_y)
		if pixel_size == 1:
			menu_font = font_x1
		elif pixel_size == 2:
			menu_font = font_x2
		elif pixel_size == 3:
			menu_font = font_x3
		else:
			menu_font = font_x4

		y = self.top_left_y - (12 * pixel_size)

		range_y = 16
		for button in self.buttons:
			y += (range_y * pixel_size)
			blit_text(button, menu_font, green, [self.top_left_x + 16, y])

	def update(self, dt, key, interact):
		self.cursor.update(dt, key)
		selected = ""

		if interact:
			for button_pos in self.button_dicts:
				if self.cursor.pos[1] == button_pos:
					selected = self.button_dicts[button_pos]

		if key[pg.K_UP] and self.cursor.pos[1] == 0:
			self.cursor.pos[1] = self.bottom + self.plus_value

		elif key[pg.K_DOWN] and self.cursor.pos[1] == self.bottom:
			self.cursor.pos[1] = 0 - self.plus_value

		return selected