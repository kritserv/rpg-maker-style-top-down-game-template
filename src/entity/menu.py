import pygame as pg
from src import font_x1, font_x2, font_x3, blit_text
from src.variable import green

class Menu:
	def __init__(self, cursor):
		self.cursor = cursor
		self.buttons = []
		self.button_dicts = {}
		self.plus_value = 10

	def calculate_menu_obs_pos(self):
		self.top = -32
		top = [-16, self.top, 16, 16]
		self.bottom = (len(self.buttons) - 1) * 16
		bottom = [-16, self.bottom, 16, 16]
		self.cursor.obs = [top, bottom]
		self.cursor.calculate_obs_pos()

	def calculate_button_pos(self):
		for i in range(len(self.buttons)):
			button_pos = i*16
			self.button_dicts[button_pos] = self.buttons[i]

	def setup_buttons(self):
		self.calculate_menu_obs_pos()
		self.calculate_button_pos()

	def resize(self, pixel_size):
		self.cursor.resize(pixel_size)

	def draw(self, pixel_size):
		self.cursor.draw(pixel_size)
		if pixel_size == 1:
			menu_font = font_x1
		elif pixel_size == 2:
			menu_font = font_x2
		else:
			menu_font = font_x3

		y = self.cursor.y - (12 * pixel_size)
		range_y = 16
		for button in self.buttons:
			y += (range_y * pixel_size)
			blit_text(button, menu_font, green, [16, y])

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
		else:
			if self.cursor.pos[1] <= -16:
				self.cursor.pos[1] = self.bottom + self.plus_value

		if selected:
			return selected
		else:
			return None