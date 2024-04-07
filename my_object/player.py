import pygame as pg
from .func import correct_all_rect, calculate_movement, calculate_obs_position, expect_finish_pos, get_distance_between, move, resize_pixel

class Player(pg.sprite.Sprite):
	def __init__(self, screen):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.speed = 150
		self.original_width, self.original_height, self.width, self.height = 16, 16, 16, 16
		self.pos = [0, 0]
		self.finish_pos = [0, 0]
		self.last_dx, self.last_dy = 0, 0
		self.rects = []
		self.x, self.y = screen.get_width()/2, screen.get_height()/2
		self.obs = []
		self.finished_x_move, self.finished_y_move = True, True
										  
	def calculate_obs_pos(self):
		self.obs = calculate_obs_position(self.obs)

	def resize(self, pixel_size):
		resize_pixel(self, pixel_size)
		self.transformed_rects = correct_all_rect(self, pixel_size)

	def draw(self, pixel_size, camera):
		for rect, color in self.transformed_rects:
			if not camera.follow_player_x_left:
				if camera.stop_follow_player_x_at_pos_left:
					if camera.player.pos[0] < camera.stop_follow_player_x_at_pos_left:
						offset_x = (camera.player.pos[0] - camera.stop_follow_player_x_at_pos_left) * pixel_size
						rect[0] += offset_x

			elif not camera.follow_player_x_right:
				if camera.stop_follow_player_x_at_pos_right:
					if camera.player.pos[0] > camera.stop_follow_player_x_at_pos_right:
						offset_x = (camera.player.pos[0] - camera.stop_follow_player_x_at_pos_right) * pixel_size
						rect[0] += offset_x
			pg.draw.rect(self.screen, color, rect)

	def update(self, dt):
		key = pg.key.get_pressed()
		dx, dy = calculate_movement(self, key)

		if dt > 0.02:
			dt = 0.02

		if self.key_presed:
			move(self.pos, dx, dy, dt, self.speed)

		if not self.key_presed:
			self.finish_pos = expect_finish_pos(self)
			self.diff_x, self.diff_y = get_distance_between(self.pos, self.finish_pos)
			
			continue_move_value = 3

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
