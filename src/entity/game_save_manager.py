from src import white, font_x1, font_x2, font_x3, font_x4, blit_text

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

	def curr_slot_have_img(self, cursor_pos):
		try:
			test = self.save_dict[str(cursor_pos)]["img_x1"]
			return True
		except KeyError:
			return False

	def draw_img(self, cursor_pos, screen, pixel_size, black_bar):
		x = self.save_menu.cursor.original_width * pixel_size + 8
		if black_bar.is_exist:
			x += black_bar.black_bar_width
		y = 0
		if self.curr_slot_have_img(cursor_pos):
			save_time = self.save_dict[str(cursor_pos)]["time"]
			level = f"Level: {self.save_dict[str(cursor_pos)]['level']}"
			scene = f"Scene: {self.save_dict[str(cursor_pos)]['new_scene'][2]}"
			if pixel_size == 1:
				use_font = font_x1
				use_image = self.save_dict[str(cursor_pos)]["img_x1"]
			elif pixel_size == 2:
				use_font = font_x2
				use_image = self.save_dict[str(cursor_pos)]["img_x2"]
			elif pixel_size == 3:
				use_font = font_x3
				use_image = self.save_dict[str(cursor_pos)]["img_x3"]
			else:
				use_font = font_x4
				use_image = self.save_dict[str(cursor_pos)]["img_x4"]

			screen.blit(use_image, (x,y))
			blit_text(save_time, use_font, white, (x+8, y))
			y += 8 * pixel_size
			blit_text(level, use_font, white, (x+8, y))
			y += 8 * pixel_size
			blit_text(scene, use_font, white, (x+8, y))

	def draw_img_in_save_menu(self, screen, pixel_size, black_bar):
		cursor_pos = int(self.save_menu.cursor.pos[1]/16)
		self.draw_img(cursor_pos, screen, pixel_size, black_bar)

	def draw_img_in_load_menu(self, screen, pixel_size, black_bar):
		cursor_pos = int(self.load_menu.cursor.pos[1]/16)
		self.draw_img(cursor_pos, screen, pixel_size, black_bar)