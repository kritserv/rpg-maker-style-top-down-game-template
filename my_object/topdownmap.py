import pygame as pg

class TopDownMap(pg.sprite.Sprite):
	def __init__(self, screen):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.rects = []
		self.x, self.y = 0, 0

	def move(self, pixel_size, player):
		self.x = -player.location[0] * pixel_size + self.screen.get_width()/2
		self.y = -player.location[1] * pixel_size + self.screen.get_height()/2

	def resize(self, pixel_size, player):
		tile_size = pixel_size*16
		map_offset = tile_size/2

		self.transformed_rects = [(pg.Rect(rect.x * pixel_size + self.x + map_offset,
										  rect.y * pixel_size + self.y + map_offset,
										  rect.width * pixel_size,
										  rect.height * pixel_size), color) for rect, color in self.rects]

	def draw(self):
		for rect, color in self.transformed_rects:
			pg.draw.rect(self.screen, color, rect)

	def update(self, pixel_size, player):
		self.move(pixel_size, player)
