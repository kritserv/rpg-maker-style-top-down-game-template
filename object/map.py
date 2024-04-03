import pygame as pg

class TopDownMap(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.rects = []
		self.rect_x, self.rect_y = 0, 0

	def add_rect(self, rect, color):
		self.rects.append((rect, color))

	def move(self, pixel_size, player, screen):

		self.rect_x = -player.location[0] * pixel_size + screen.get_width()/2
		self.rect_y = -player.location[1] * pixel_size + screen.get_height()/2

	def resize(self, pixel_size, player, screen):

		tile_size = pixel_size*16
		map_offset = tile_size/2

		self.transformed_rects = [(pg.Rect(rect.x * pixel_size + self.rect_x + map_offset,
										  rect.y * pixel_size + self.rect_y + map_offset,
										  rect.width * pixel_size,
										  rect.height * pixel_size), color) for rect, color in self.rects]

	def draw(self, screen):
		for rect, color in self.transformed_rects:
			pg.draw.rect(screen, color, rect)

	def update(self, pixel_size, player, screen):
		self.move(pixel_size, player, screen)