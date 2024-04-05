import pygame as pg
from math import floor, ceil

class Player(pg.sprite.Sprite):
	def __init__(self, screen):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.speed = 150
		self.original_width, self.original_height, self.width, self.height = 16, 16, 16, 16
		self.pos = [0, 0]
		self.last_dx, self.last_dy = 0, 0
		self.rects = []
		self.x, self.y = screen.get_width()/2, screen.get_height()/2
		self.obs = []

	def correct_all_rect(self, pixel_size):
		self.transformed_rects = [(pg.Rect(rect.x * pixel_size + self.top_left_x,
										  rect.y * pixel_size + self.top_left_y,
										  rect.width * pixel_size,
										  rect.height * pixel_size), color) for rect, color in self.rects]
										  
	def calculate_obs_pos(self):
		plus_value = 10
		calculated_obs = []
		for ob in self.obs:
			ob_values = {
				"left": [ob[2] + ob[0] + 16 - plus_value, ob[2] + ob[0] + 32 - plus_value, ob[1] + 16, ob[3] + ob[1]],
				"right": [ob[0] - plus_value, ob[0] + 16 - plus_value, ob[1] + 16, ob[3] + ob[1]],
				"up": [ob[0] + 16, ob[2] + ob[0], ob[3] + 16 - plus_value + ob[1], ob[3] + 32 - plus_value + ob[1]],
				"down": [ob[0] + 16, ob[2] + ob[0], ob[1] - plus_value, ob[1] + 16]
			}
			calculated_obs.append(ob_values)
		self.obs = calculated_obs
										  
	def ob_is_in_direction(self, direction):
		for ob in self.obs:
			if (ob[direction][0] <= self.pos[0] <= ob[direction][1]) and (ob[direction][2] <= self.pos[1] <= ob[direction][3]):
				return True
		return False

	def move_left_get_obstruct(self):
		return self.ob_is_in_direction("left")


	def move_right_get_obstruct(self):
		return self.ob_is_in_direction("right")

	def move_up_get_obstruct(self):
		return self.ob_is_in_direction("up")

	def move_down_get_obstruct(self):
		return self.ob_is_in_direction("down")

	def calculate_movement(self, key):
		dx, dy = 0, 0
		self.key_presed = False

		if key[pg.K_LEFT] or key[pg.K_RIGHT]:
			if self.finished_y_move:
				if key[pg.K_LEFT] and not self.move_left_get_obstruct():
					dx = -1
				elif key[pg.K_RIGHT] and not self.move_right_get_obstruct():
					dx = 1
				if dx != 0:
					self.last_dx = dx
					self.key_presed = True
					self.finished_x_move = False
		elif key[pg.K_UP] or key[pg.K_DOWN]:
			if self.finished_x_move:
				if key[pg.K_UP] and not self.move_up_get_obstruct():
					dy = -1
				elif key[pg.K_DOWN] and not self.move_down_get_obstruct():
					dy = 1
				if dy != 0:
					self.last_dy = dy
					self.key_presed = True
					self.finished_y_move = False

		return dx, dy

	def cannot_divide_by_16(self, num):
		if num % 16 != 0:
			return True
		else:
			return False

	def make_divisible_by_16(self, num):
		if num > 0:
			while num % 16 != 0:
				num += 1
		elif num < 0:
			while num % 16 != 0:
				num -= 1
		return num

	def move(self, dx, dy, dt, pixel_size):
		self.pos[0] += dx * self.speed * dt
		self.pos[1] += dy * self.speed * dt

	def expect_finish_pos(self):
		if self.last_dx < 0:
			checker = floor(self.pos[0])
		elif self.last_dx > 0:
			checker = ceil(self.pos[0])
		else:
			checker = 0

		if self.cannot_divide_by_16(checker):
			self.expected_x = self.make_divisible_by_16(checker)
		if checker == 0:
			self.expected_x = 0

		if self.last_dy < 0:
			checker = floor(self.pos[1])
		elif self.last_dy > 0:
			checker = ceil(self.pos[1])
		else:
			checker = 0

		if self.cannot_divide_by_16(checker):
			self.expected_y = self.make_divisible_by_16(checker)
		if checker == 0:
			self.expected_y = 0

	def get_different_of_current_and_expected_pos(self):
		if self.pos[0] > self.expected_x:
			self.diff_x = self.pos[0] - self.expected_x
		elif self.pos[0] < self.expected_x:
			self.diff_x = self.expected_x - self.pos[0]
		else:
			self.diff_x = 0

		if self.pos[1] > self.expected_y:
			self.diff_y = self.pos[1] - self.expected_y
		elif self.pos[1] < self.expected_y:
			self.diff_y = self.expected_y - self.pos[1]
		else:
			self.diff_y = 0

	def resize(self, pixel_size):
		screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
		self.x, self.y = screen_width/2, screen_height/2
		self.width, self.height = self.original_width * pixel_size, self.original_height * pixel_size
		self.top_left_x, self.top_left_y = self.x - self.width/2, self.y - self.height/2

		self.correct_all_rect(pixel_size)

	def draw(self):
		for rect, color in self.transformed_rects:
			pg.draw.rect(self.screen, color, rect)

	def update(self, dt, pixel_size):
		key = pg.key.get_pressed()
		dx, dy = self.calculate_movement(key)

		if dt > 0.02:
		    dt = 0.02

		if self.key_presed:
			self.move(dx, dy, dt, pixel_size)

		if not self.key_presed:
			self.expect_finish_pos()
			self.get_different_of_current_and_expected_pos()

			continue_move_value = 3

			if self.diff_x > continue_move_value:
				self.move(self.last_dx, 0, dt, pixel_size)
			elif self.diff_x <= continue_move_value:
				self.pos[0] = self.expected_x
				self.finished_x_move = True

			if self.diff_y > continue_move_value:
				self.move(0, self.last_dy, dt, pixel_size)
			elif self.diff_y <= continue_move_value:
				self.pos[1] = self.expected_y
				self.finished_y_move = True
