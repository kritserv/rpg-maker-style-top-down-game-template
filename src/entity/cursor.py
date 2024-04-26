import pygame as pg
from .ent_func import correct_all_rect, calculate_movement, calculate_obs_position, expect_finish_pos, get_distance_between, move, resize_pixel
from src.variable import white

continue_move_value = 3

class Cursor:
	def __init__(self, screen):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.speed = 120
		self.original_width, self.original_height, self.width, self.height = 160, 16, 160, 16
		self.pos = [0, 0]
		self.finish_pos = [0, 0]
		self.last_dx, self.last_dy = 0, 0
		self.rects = [
			(pg.Rect(0, 0, 16, 16), white), 
		]
		self.x, self.y = screen.get_width()/2, screen.get_height()/2
		self.obs = []
		self.finished_x_move, self.finished_y_move = True, True
		self.resize_cache_dict = {}
										  
	def calculate_obs_pos(self):
		self.obs = calculate_obs_position(self.obs)

	def resize(self, pixel_size):
		resize_pixel(self, pixel_size)
		self.transformed_rects = correct_all_rect(self, pixel_size)

	def draw(self, pixel_size):
		pg.draw.rect(self.screen, white, pg.Rect(8+(self.pos[0]*pixel_size), (self.pos[1]*pixel_size)+self.y, self.original_width*pixel_size, self.original_height*pixel_size))

	def update(self, dt, key):
		dx, dy = calculate_movement(self, key)

		if self.key_presed:
			move(self.pos, dx, dy, dt, self.speed)

		if not self.key_presed:

			self.finish_pos = expect_finish_pos(self, continue_move_value)
			self.diff_x, self.diff_y = get_distance_between(self.pos, self.finish_pos)

			if self.diff_x > continue_move_value:
				move(self.pos, self.last_dx, 0, dt, self.speed)
			elif self.diff_x <= continue_move_value:
				self.pos[0] = self.finish_pos[0]
				self.finished_x_move = True

			if self.diff_y > continue_move_value:
				move(self.pos, 0, self.last_dy, dt, self.speed)
			elif self.diff_y <= continue_move_value:
				self.pos[1] = self.finish_pos[1]
				self.finished_y_move = True
