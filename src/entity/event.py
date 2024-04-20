class Event:
	def __init__(self, event_dict, player, scene_manager):
		self.event_dict = event_dict
		self.player = player
		self.scene_manager = scene_manager

	def trigger(self, effect):
		for func in effect["func"]:
			if func == "change_scene":
				x, y, new_scene_name = effect["new_scene"]
				self.scene_manager.change_scene(x, y, new_scene_name)
			elif func == "change_camera_stop_position":
				stop_left, stop_right, stop_up, stop_down = effect["new_camera_stop_position"]
				self.scene_manager.change_camera_stop_position(stop_left, stop_right, stop_up, stop_down)

	def check_condition(self):
		for scene_event in self.event_dict[self.scene_manager.current_scene]:
			if scene_event["trigger_by"] == "player_on_top":
				if self.player.pos == scene_event["pos"]:
					self.trigger(scene_event["effect"])
					break

	def update(self):
		self.check_condition()