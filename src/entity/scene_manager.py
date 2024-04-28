from .ent_func import changing_scene, changing_camera_stop_position

class SceneManager:
	def __init__(self, scene_dict, player, tdmap, camera):
		self.scene_dict = scene_dict
		self.player = player
		self.tdmap = tdmap
		self.camera = camera
		self.cache_dict = {}
		self.current_scene = ""

	def change_scene(self, x, y, new_scene_name):
		changing_scene(self, x, y, new_scene_name)

	def change_camera_stop_position(self, stop_left, stop_right, stop_up, stop_down):
		changing_camera_stop_position(self.camera, stop_left, stop_right, stop_up, stop_down)