import pygame as pg

class Menu:
	def __init__(self, cursor):
		self.cursor = cursor
		self.buttons = []
		self.button_dicts = {}
		self.selected = ""
		self.plus_value = 10

	def calculate_obs_pos(self):
		top = [-16, -32, 16, 16]
		self.bottom = (len(self.buttons) - 1) * 16
		bottom = [-16, self.bottom, 16, 16]
		self.cursor.obs = [top, bottom]
		self.cursor.calculate_obs_pos()

	def calculate_button_pos(self):
		for i in range(len(self.buttons)):
			button_pos = i*16
			self.button_dicts[button_pos] = self.buttons[i]

	def setup_buttons(self):
		self.calculate_obs_pos()
		self.calculate_button_pos()

	def resize(self, pixel_size):
		self.cursor.resize(pixel_size)

	def draw(self, pixel_size):
		self.cursor.draw(pixel_size)

	def update(self, dt, key):
		self.cursor.update(dt, key)

		if key[pg.K_RETURN]:
			for button_pos in self.button_dicts:
				if self.cursor.pos[1] == button_pos:
					self.selected = self.button_dicts[button_pos]

		if key[pg.K_UP] and self.cursor.pos[1] == 0:
				self.cursor.pos[1] = self.bottom + self.plus_value

		elif key[pg.K_DOWN] and self.cursor.pos[1] == self.bottom:
				self.cursor.pos[1] = 0 - self.plus_value

		if self.selected:
			return self.selected
		else:
			return None