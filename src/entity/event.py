class Event:
	def __init__(self, event_dict, player, scene_manager):
		self.event_dict = event_dict
		self.player = player
		self.scene_manager = scene_manager

	def trigger_change_scene_event(self, new_scene):
		x, y, new_scene_name = new_scene
		self.scene_manager.change_scene(x, y, new_scene_name)

	def trigger_change_cam_event(self, new_camera_stop_position):
		stop_left, stop_right, stop_up, stop_down = new_camera_stop_position
		self.scene_manager.change_camera_stop_position(stop_left, stop_right, stop_up, stop_down)

	def trigger(self, effect):
		func = effect["func"]
		if func == "change_scene":
			self.trigger_change_scene_event(effect["new_scene"])
			self.trigger_change_cam_event(effect["new_camera_stop_position"])

	def check_condition(self):
		for scene_event in self.event_dict[self.scene_manager.current_scene]:
			if scene_event["trigger_by"] == "player_on_top":
				if self.player.pos == scene_event["pos"]:
					self.trigger(scene_event["effect"])
					break

	def update(self):
		self.check_condition()