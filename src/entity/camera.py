from .ent_func import move_map, follow_or_stop_follow

class Camera:
	def __init__(self, player, tdmap, renderer):
		self.player = player
		self.tdmap = tdmap
		self.renderer = renderer

	def draw(self, screen, current_scene, pixel_size):
		if self.renderer.rendering:
			self.renderer.render_scene_behind_player(screen, self.tdmap, current_scene, pixel_size)
			self.tdmap.draw()
			self.player.draw(pixel_size, self)
			self.renderer.render_scene_in_front_of_player(screen, self.tdmap, current_scene, pixel_size)
		else:
			self.tdmap.draw()
			self.player.draw(pixel_size, self)

	def update(self, pixel_size):
		follow_or_stop_follow(self, self.player)
		move_map(self, pixel_size)