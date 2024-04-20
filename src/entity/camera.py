from .ent_func import move_map, follow_or_stop_follow

class Camera:
	def __init__(self, player, tdmap):
		self.player = player
		self.tdmap = tdmap

	def draw(self, pixel_size, player, top_down_map):
		top_down_map.draw()
		player.draw(pixel_size, self)

	def update(self, pixel_size):
		follow_or_stop_follow(self, self.player)
		move_map(self, pixel_size)