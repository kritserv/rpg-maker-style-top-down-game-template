import pygame as pg
from variable.settings import red
from object.timer import Timer
from math import floor, ceil

class Player(pg.sprite.Sprite):
	def __init__(self, screen):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.speed = 150
		self.original_width, self.original_height = 16, 16
		self.location = [0, 0]
		self.expected_x = 0
		self.expected_y = 0
		self.last_dx = 0
		self.last_dy = 0
		self.diff_x = 0
		self.diff_y = 0
		self.key_presed = False
		self.is_move = False
		self.finished_x_move = True
		self.finished_y_move = True

		screen_width, screen_height = screen.get_width(), screen.get_height()
		player_x, player_y = screen_width/2, screen_height/2
		self.x = player_x
		self.y = player_y
		self.width = self.original_width
		self.height = self.original_height
		self.top_left_x = self.x - self.width/2
		self.top_left_y = self.y - self.height/2

		self.rects = []

	def add_rect(self, rect, color):
		self.rects.append((rect, color))

	def correct_all_rect(self, pixel_size):
		self.transformed_rects = [(pg.Rect(rect.x * pixel_size + self.top_left_x,
										  rect.y * pixel_size + self.top_left_y,
										  rect.width * pixel_size,
										  rect.height * pixel_size), color) for rect, color in self.rects]

	def calculate_movement(self, key):
		dx, dy = 0, 0
		self.is_move = False
		self.key_presed = False

		if key[pg.K_LEFT] or key[pg.K_RIGHT]:
			if self.finished_y_move:
				if key[pg.K_LEFT]:
					dx = -1
				elif key[pg.K_RIGHT]:
					dx = 1
				self.is_move = True
				self.last_dx = dx
				self.key_presed = True
				self.finished_x_move = False
		elif key[pg.K_UP] or key[pg.K_DOWN]:
			if self.finished_x_move:
				if key[pg.K_UP]:
					dy = -1
				elif key[pg.K_DOWN]:
					dy = 1
				self.is_move = True
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
		self.location[0] += dx * self.speed * dt
		self.location[1] += dy * self.speed * dt


	def expect_finish_location(self):
		if self.last_dx < 0:
			checker = floor(self.location[0])
		elif self.last_dx > 0:
			checker = ceil(self.location[0])
		else:
			checker = 0

		if self.cannot_divide_by_16(checker):
			self.expected_x = self.make_divisible_by_16(checker)
		if checker == 0:
			self.expected_x = 0

		if self.last_dy < 0:
			checker = floor(self.location[1])
		elif self.last_dy > 0:
			checker = ceil(self.location[1])
		else:
			checker = 0

		if self.cannot_divide_by_16(checker):
			self.expected_y = self.make_divisible_by_16(checker)
		if checker == 0:
			self.expected_y = 0

	def calculate_diff(self):
		if self.location[0] > self.expected_x:
			self.diff_x = self.location[0] - self.expected_x
		elif self.location[0] < self.expected_x:
			self.diff_x = self.expected_x - self.location[0]
		else:
			self.diff_x = 0

		if self.location[1] > self.expected_y:
			self.diff_y = self.location[1] - self.expected_y
		elif self.location[1] < self.expected_y:
			self.diff_y = self.expected_y - self.location[1]
		else:
			self.diff_y = 0

	def finish_move(self, dx, dy, dt, pixel_size):
		self.move(dx, dy, dt, pixel_size)

	def resize(self, pixel_size):
		screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
		player_x, player_y = screen_width/2, screen_height/2
		self.x = player_x
		self.y = player_y
		self.width = self.original_width * pixel_size
		self.height = self.original_height * pixel_size
		self.top_left_x = self.x - self.width/2
		self.top_left_y = self.y - self.height/2

		self.correct_all_rect(pixel_size)

	def draw(self):
		self.rect = pg.Rect(self.top_left_x, self.top_left_y, self.width, self.height)
		pg.draw.rect(self.screen, red, self.rect)
		for rect, color in self.transformed_rects:
			pg.draw.rect(self.screen, color, rect)

	def update(self, dt, pixel_size):

		key = pg.key.get_pressed()
		dx, dy = self.calculate_movement(key)

		if self.key_presed:
			self.move(dx, dy, dt, pixel_size)

		if not self.key_presed:
			self.expect_finish_location()
			self.calculate_diff()

			if self.diff_x >= 0.7:
				self.finish_move(self.last_dx, 0, dt, pixel_size)
			elif self.diff_x < 0.7:
				self.location[0] = self.expected_x
				self.finished_x_move = True

			if self.diff_y >= 0.7:
				self.finish_move(0, self.last_dy, dt, pixel_size)
			elif self.diff_y < 0.7:
				self.location[1] = self.expected_y
				self.finished_y_move = True