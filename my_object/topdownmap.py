import pygame as pg
from .func import move_map, correct_all_map_rect

class TopDownMap(pg.sprite.Sprite):
	def __init__(self, screen):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.rects = []
		self.x, self.y = 0, 0

	def resize(self, pixel_size, player):
		self.transformed_rects = correct_all_map_rect(self, pixel_size)

	def draw(self, follow_player_x, follow_player_y, pixel_size):
		for rect, color in self.transformed_rects:
			pg.draw.rect(self.screen, color, rect)

	def update(self, pixel_size, player, follow_player_x, follow_player_y):
		move_map(self, pixel_size, player, follow_player_x, follow_player_y)