class SceneManager:
	def __init__(self, scene_dict, player, tdmap, camera):
		self.scene_dict = scene_dict
		self.player = player
		self.tdmap = tdmap
		self.camera = camera
			
	def change_scene(self, x, y, new_scene_name):
		self.player.obs = [ob for ob, color in self.scene_dict[new_scene_name]]
		self.player.calculate_obs_pos()
		self.player.pos = [x, y]
		self.player.finish_pos = [x, y]
		self.tdmap.rects = [ob for ob in self.scene_dict[new_scene_name]]
		self.current_scene = new_scene_name

	def change_camera_stop_position(self, stop_left, stop_right, stop_up, stop_down):
		self.camera.stop_follow_player_left_at_pos_x = stop_left
		self.camera.stop_follow_player_right_at_pos_x = stop_right
		self.camera.stop_follow_player_up_at_pos_y = stop_up
		self.camera.stop_follow_player_down_at_pos_y = stop_down