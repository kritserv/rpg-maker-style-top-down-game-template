class Renderer:
	def __init__(self, scene_asset):
		self.scene_asset = scene_asset
		self.rendering = True

	def display_img(self, screen, tdmap, layer, pixel_size):
		for imgs_and_pos in layer:
			img_x1, img_x2, img_x3, pos = imgs_and_pos
			if pixel_size == 1:
				use_img = img_x1
			elif pixel_size == 2:
				use_img = img_x2
			elif pixel_size == 3:
				use_img = img_x3
			screen.blit(use_img, (tdmap.x + (pos[0] * pixel_size), tdmap.y + (pos[1] * pixel_size)))

	def render_scene_behind_player(self, screen, tdmap, current_scene, pixel_size):
		current_asset = self.scene_asset[current_scene]
		if current_asset["behind_player"]:
			self.display_img(screen, tdmap, current_asset["behind_player"], pixel_size)

	def render_scene_in_front_of_player(self, screen, tdmap, current_scene, pixel_size):
		current_asset = self.scene_asset[current_scene]
		if current_asset["in_front_of_player"]:
			self.display_img(screen, tdmap, current_asset["in_front_of_player"], pixel_size)