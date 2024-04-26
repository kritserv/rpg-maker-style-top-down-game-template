class SaveManager:
	def __init__(self, save_dict):
		self.save_dict = save_dict

	def create_buttons(self):
		for i in range(len(self.save_dict)):
			self.save_menu.buttons.append(f"Save To Slot {i}")
			self.load_menu.buttons.append(f"Load From Slot {i}")

		self.save_menu.buttons.append("Cancel")
		self.load_menu.buttons.append("Cancel")
		self.save_menu.setup_buttons()
		self.load_menu.setup_buttons()