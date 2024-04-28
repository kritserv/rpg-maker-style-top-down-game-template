class SaveManager:
	def __init__(self, save_dict):
		self.save_dict = save_dict

	def create_buttons(self):
		for i in range(len(self.save_dict)):

			if self.save_dict[str(i)]:
				self.load_menu.buttons.append(f"Load Slot {i}")
				self.save_menu.buttons.append(f"Overwrite Slot {i}")
			else:
				self.load_menu.buttons.append(f"Slot {i} Empty")
				self.save_menu.buttons.append(f"Slot {i} Empty")

		self.save_menu.buttons.append("Cancel")
		self.load_menu.buttons.append("Cancel")
		self.save_menu.setup_buttons()
		self.load_menu.setup_buttons()

	def refresh_save_slot(self):
		self.load_menu.buttons = []
		self.save_menu.buttons = []
		self.create_buttons()