from .ent_func import move_map, follow_or_stop_follow

class Camera:
	def __init__(self, player, tdmap):
		self.player = player
		self.tdmap = tdmap
		self.follow_player_x_left = True
		self.follow_player_x_right = True
		self.follow_player_y_up = True
		self.follow_player_y_down = True
		self.stop_follow_player_left_at_pos_x = None
		self.stop_follow_player_right_at_pos_x = None
		self.stop_follow_player_up_at_pos_y = None
		self.stop_follow_player_down_at_pos_y = None

	def draw(self, pixel_size, player, top_down_map):
		top_down_map.draw()
		player.draw(pixel_size, self)

	def update(self, pixel_size):
		follow_or_stop_follow(self, self.player)
		move_map(self, pixel_size)