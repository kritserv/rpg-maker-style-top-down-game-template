class Event:
	def __init__(self, event_dict, player, scene_manager):
		self.event_dict = event_dict
		self.player = player
		self.scene_manager = scene_manager

		self.draw_text_box = False
		self.current_text_list = []
		self.current_text_index = 0

	def is_near(self, player_pos, event_pos):
		tile_size = 16
		positions_to_check = [
			[event_pos[0], event_pos[1] + tile_size],
			[event_pos[0], event_pos[1] - tile_size],
			[event_pos[0] + tile_size, event_pos[1]],
			[event_pos[0] - tile_size, event_pos[1]]
		]

		near = False
		if player_pos in positions_to_check:
			near = True
			return near

		return near

	def trigger_change_scene_event(self, new_scene):
		x, y, new_scene_name = new_scene
		self.scene_manager.change_scene(x, y, new_scene_name)

	def trigger_change_cam_event(self, new_camera_stop_position):
		stop_left, stop_right, stop_up, stop_down = new_camera_stop_position
		self.scene_manager.change_camera_stop_position(stop_left, stop_right, stop_up, stop_down)

	def trigger_show_text_event(self, text_list):
		self.draw_text_box = True
		self.current_text_list = text_list

	def trigger(self, effect):
		func = effect["func"]
		if func == "change_scene":
			self.trigger_change_scene_event(effect["new_scene"])
			self.trigger_change_cam_event(effect["new_camera_stop_position"])
		elif func == "show_text":
			self.trigger_show_text_event(effect["text_list"])

	def check_condition(self, interact):
		for scene_event in self.event_dict[self.scene_manager.current_scene]:
			if scene_event["trigger_by"] == "player_on_top":
				if self.player.pos == scene_event["pos"]:
					self.trigger(scene_event["effect"])
			elif scene_event["trigger_by"] == "player_on_top_and_interact":
				if self.player.pos == scene_event["pos"] and interact:
					self.trigger(scene_event["effect"])
			elif scene_event["trigger_by"] == "player_is_near_and_interact":
				if self.is_near(self.player.pos, scene_event["pos"]) and interact:
					self.trigger(scene_event["effect"])

	def update(self, interact):
		if not self.draw_text_box:
			self.check_condition(interact)
		else:
			self.player.disable_move = True
			if interact:
				self.current_text_index += 1
			if self.current_text_index >= len(self.current_text_list):
				self.current_text_index = 0
				self.draw_text_box = False
				self.player.disable_move = False