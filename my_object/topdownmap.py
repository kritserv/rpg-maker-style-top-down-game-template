import pygame as pg
from .func import correct_all_map_rect

class TopDownMap(pg.sprite.Sprite):
	def __init__(self, screen, current_scene):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.rects = []
		self.x, self.y = 0, 0
		self.current_scene = current_scene

	def resize(self, pixel_size, player):
		self.transformed_rects = correct_all_map_rect(self, pixel_size)

	def draw(self):
		for rect, color in self.transformed_rects:
			pg.draw.rect(self.screen, color, rect)