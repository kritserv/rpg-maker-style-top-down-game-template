from .func import move_map

class Camera:
	def __init__(self, player, tdmap):
		self.player = player
		self.tdmap = tdmap
		self.follow_player_x_left = True
		self.follow_player_x_right = True
		self.follow_player_y = True
		self.stop_follow_player_x_at_pos_left = None
		self.stop_follow_player_x_at_pos_right = None
		self.stop_follow_player_y_at_pos_up = None
		self.stop_follow_player_y_at_pos_down = None

	def draw(self, pixel_size, player, top_down_map):
		top_down_map.draw()
		player.draw(pixel_size, self)

	def update(self, pixel_size):
		if self.stop_follow_player_x_at_pos_left:
			if self.player.pos[0] < self.stop_follow_player_x_at_pos_left:
				self.follow_player_x_left = False
			else:
				self.follow_player_x_left = True

		if self.stop_follow_player_x_at_pos_right:
				if self.player.pos[0] > self.stop_follow_player_x_at_pos_right:
					self.follow_player_x_right = False
				else:
					self.follow_player_x_right = True


		move_map(self, pixel_size)