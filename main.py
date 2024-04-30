import pygame as pg
pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
from sys import exit
import asyncio
from time import time
from src import clock_tick, curr_fps,\
	default_screen_width, \
	default_screen_height, \
	default_screen_size, \
	black, darkblue, \
	check_pygame_event, \
	load_screen_from_json, save_screen_setting, \
	toggle_full_screen, update_size, \
	load_scene_from_json, load_event_from_json, \
	load_save_from_json, save_player_data, \
	load_asset, \
	Player, TopDownMap, Camera, BlackBar, \
	Timer, SceneManager, SaveManager, Event, \
	Cursor, Menu, Debugger, TextBox

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

async def main():
	running = True
	web_export = False
	debug = False
	debug_list = [""]
	full_screen_toggle = False
	pause = False
	pause_toggle = False
	full_screen_size = pg.display.get_desktop_sizes()[0]
	screen, \
	full_screen, \
	black_bar_is_set, \
	cap_fps, \
	target_fps = load_screen_from_json()
	black_bar = BlackBar(screen, black_bar_is_set)
	curr_width, curr_height, pixel_size = update_size(
		[
			screen.get_width(), 
			screen.get_height()
			]
		)
	ratio = default_screen_width/default_screen_height
	new_size = (curr_width, curr_height)

	if web_export:
		cap_fps = True

	player = Player(screen)
	top_down_map = TopDownMap(screen)
	camera = Camera(player, top_down_map)
	text_box = TextBox(screen)

	town1_img_x1, town1_img_x2, town1_img_x3 = load_asset()
	town1_offset_x = -208+8
	town1_offset_y = -176-8

	scene_manager = SceneManager(
		load_scene_from_json(), player, top_down_map, camera
		)

	event_dict, start_event = load_event_from_json()
	event = Event(
		event_dict, player, scene_manager
		)

	save_manager = SaveManager(load_save_from_json())
	save_manager.save_menu, save_manager.load_menu = Menu(
		Cursor(screen)), Menu(Cursor(screen)
		)
	save_manager.create_buttons()
	loadable_slot = []
	savable_slot = []
	overwritable_slot = []
	screenshot = False

	for i in range(8):
		loadable_slot.append(f"Load Slot {i}")
		savable_slot.append(f"Slot {i} Empty")
		overwritable_slot.append(f"Overwrite Slot {i}")

	title_screen_menu = Menu(Cursor(screen))
	title_screen_menu.buttons = [
		"Start Game", "Load Game", "Options", "Quit Game"
		]
	title_screen_menu.setup_buttons()
	title_screen_menu.font_size_plus_05 = True

	options_menu = Menu(Cursor(screen))
	if full_screen:
		initial_screen = "Full Screen"
	else:
		initial_screen = "Window"
	if not cap_fps:
		initial_fps = "No Limit Fps"
	else:
		initual_fps = f"Cap Fps At {target_fps}"
	if black_bar_is_set:
		initial_blackbar = "Black Bar: On"
	else:
		initial_blackbar = "Black Bar: Off"
	options_menu.buttons = [
		initial_screen, 
		initial_fps, 
		initial_blackbar, 
		"Apply", 
		"Back"
		]
	old_options = options_menu.buttons.copy()
	options_menu.setup_buttons()
	options_menu.font_size_plus_05 = True

	pause_menu = Menu(Cursor(screen))
	pause_menu.buttons = [
		"Save", "Load", "Options", "Back To Title", "Cancel"
		]
	pause_menu.setup_buttons()
	pause_menu.font_size_plus_05 = True

	game_state = "title_screen_menu"
	old_game_state = "title_screen_menu"

	debugger = Debugger()

	debug_timer = Timer()
	debug_timer.start()

	prev_time = time()
	while running:

		# ================== [ DELTA TIME ] ==================

		dt = time() - prev_time
		prev_time = time()

		# =================== [ GET INPUT ] ===================

		running, \
		new_size, \
		debug, \
		full_screen_toggle, \
		pause_toggle, \
		interact, \
		cancel = check_pygame_event(
			pg.event.get(), new_size, debug
			)
		curr_width, curr_height, pixel_size = update_size(
			new_size
			)
		key = pg.key.get_pressed()

		# =============== [ TOGGLE THE TOGGLEABLE ] ===============

		if pause_toggle:
			pause_toggle = False
			if not event.draw_text_box:
				pause = not pause

		if full_screen_toggle:
			full_screen = not full_screen
			if full_screen:
				screen = toggle_full_screen(
					full_screen_size, default_screen_size
				)
			else:
				screen = toggle_full_screen(
					new_size, default_screen_size
				)
			full_screen_toggle = False

		# ================= [ GET GAME STATE ] =================

		if game_state == "title_screen_menu":
			old_game_state = "title_screen_menu"
			pause = False

			# ================== [ TITLE LOGIC ] ================

			selected = title_screen_menu.update(dt, key, interact)
			if selected == "Start Game":
				event.trigger(start_event["effect"])
				game_state = "main_game"
				title_screen_menu.reset_cursor()
			elif selected == "Load Game":
				game_state = "load_game_menu"
			elif selected == "Options":
				game_state = "options_menu"
			elif selected == "Quit Game":
				running = False

			# ================= [ TITLE GRAPHIC ] ================

			screen.fill(darkblue)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			title_screen_menu.draw(pixel_size, black_bar)

		elif game_state == "main_game":
			old_game_state = "main_game"

			# ================= [ MAIN LOGIC ] =================

			camera.update(pixel_size)
			if not pause:
				player.update(dt, key)
				event.update(interact)
				if event.draw_text_box:
					text_in_text_box = event.current_text_list[event.current_text_index]
			else:

				# ============= [ PAUSE MENU LOGIC ] ==============

				old_game_state = "pause_menu"
				selected = pause_menu.update(dt, key, interact)
				if selected == "Save":
					game_state = "save_game_menu"
				elif selected == "Load":
					game_state = "load_game_menu"
				elif selected == "Options":
					game_state = "options_menu"
				elif selected == "Back To Title":
					game_state = "title_screen_menu"
					pause_menu.reset_cursor()
				elif selected == "Cancel":
					pause = False
					pause_menu.reset_cursor()

			# ================= [ MAIN GRAPHIC ] ===============

			player.resize(pixel_size)
			top_down_map.resize(pixel_size, player)

			screen.fill(darkblue)
			if scene_manager.current_scene == "town1":
				if pixel_size == 1:
					screen.blit(town1_img_x1, (camera.tdmap.x + (town1_offset_x * pixel_size), camera.tdmap.y + (town1_offset_y * pixel_size)))
				elif pixel_size == 2:
					screen.blit(town1_img_x2, (camera.tdmap.x + (town1_offset_x * pixel_size), camera.tdmap.y + (town1_offset_y * pixel_size)))
				elif pixel_size == 3:
					screen.blit(town1_img_x3, (camera.tdmap.x + (town1_offset_x * pixel_size), camera.tdmap.y + (town1_offset_y * pixel_size)))
			camera.draw(pixel_size, player, top_down_map)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			if event.draw_text_box:
				text_box.draw(pixel_size, black_bar, text_in_text_box)
			if pause:
				if not screenshot:
					screenshot = screen.copy()
					screenshot = pg.transform.scale(screenshot, (240, 160))
				pause_menu.draw(pixel_size, black_bar)
			else:
				screenshot = False

		elif game_state == "load_game_menu":

			# ================ [ LOAD GAME LOGIC ] ==============

			selected = save_manager.load_menu.update(dt, key, interact)
			for i, slot in enumerate(loadable_slot):
				if selected == slot:
					event.trigger(save_manager.save_dict[str(i)])
					player.level = save_manager.save_dict[str(i)]["level"]
					player.items = save_manager.save_dict[str(i)]["items"]
					game_state = "main_game"
					pause = False
					save_manager.load_menu.reset_cursor()
			if selected == "Cancel" or cancel:
				if old_game_state == "pause_menu":
					game_state = "main_game"
					pause = True
				else:
					game_state = old_game_state
				save_manager.load_menu.reset_cursor()

			# =============== [ LOAD GAME GRAPHIC ] ==============

			screen.fill(darkblue)
			save_manager.draw_img_in_load_menu(screen, pixel_size, black_bar)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			save_manager.load_menu.draw(pixel_size, black_bar)

		elif game_state == "save_game_menu":

			# ================ [ SAVE GAME LOGIC ] ==============

			selected = save_manager.save_menu.update(dt, key, interact)
			for i, slot in enumerate(savable_slot):
				if selected == slot:
					save_player_data(player, scene_manager.current_scene, i, screenshot)
					save_manager.save_dict = load_save_from_json()
					save_manager.refresh_save_slot()

			for i, slot in enumerate(overwritable_slot):
				if selected == slot:
					save_player_data(player, scene_manager.current_scene, i, screenshot)
					save_manager.save_dict = load_save_from_json()
					save_manager.refresh_save_slot()

			if selected == "Cancel" or cancel:
				if old_game_state == "pause_menu":
					game_state = "main_game"
					pause = True
				else:
					game_state = old_game_state
				save_manager.save_menu.reset_cursor()
				screenshot = False

			# =============== [ SAVE GAME GRAPHIC ] ==============

			screen.fill(darkblue)
			save_manager.draw_img_in_save_menu(screen, pixel_size, black_bar)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			save_manager.save_menu.draw(pixel_size, black_bar)

		elif game_state == "options_menu":

			# ================ [ OPTIONS LOGIC ] ==============

			selected = options_menu.update(dt, key, interact)
			if selected == "Window":
				options_menu.buttons[0] = "Full Screen"
				options_menu.refresh_text()
			elif selected == "Full Screen":
				options_menu.buttons[0] = "Window"
				options_menu.refresh_text()
			elif selected == "No Limit Fps":
				options_menu.buttons[1] = "Cap Fps At 60"
				options_menu.refresh_text()
			elif selected == "Cap Fps At 60":
				options_menu.buttons[1] = "Cap Fps At 90"
				options_menu.refresh_text()
			elif selected == "Cap Fps At 90":
				options_menu.buttons[1] = "Cap Fps At 144"
				options_menu.refresh_text()
			elif selected == "Cap Fps At 144":
				options_menu.buttons[1] = "No Limit Fps"
				options_menu.refresh_text()
			elif selected == "Black Bar: Off":
				options_menu.buttons[2] = "Black Bar: On"
				options_menu.refresh_text()
			elif selected == "Black Bar: On":
				options_menu.buttons[2] = "Black Bar: Off"
				options_menu.refresh_text()
			elif selected == "Apply":
				full_screen_setting = options_menu.buttons[0] == "Full Screen"
				cap_fps_setting = options_menu.buttons[1] != "No Limit Fps"
				target_fps_setting = 60
				if cap_fps_setting:
					target_fps_setting = int(options_menu.buttons[1].split(" ")[3])
				black_bar_setting = options_menu.buttons[2] == "Black Bar: On"
				save_screen_setting(
					full_screen_setting, 
					black_bar_setting, 
					cap_fps_setting, 
					target_fps_setting
					)
				if full_screen_setting:
					screen = pg.display.set_mode(full_screen_size, pg.FULLSCREEN)
				else:
					screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
				black_bar.screen = screen
				text_box.screen = screen

				if black_bar_setting:
					black_bar.is_exist = True
				else:
					black_bar.is_exist = False

				if cap_fps_setting:
					cap_fps = True
				else:
					cap_fps = False

				target_fps = target_fps_setting
				
				for menu in [
					options_menu, 
					pause_menu, 
					save_manager.save_menu, 
					save_manager.load_menu, 
					title_screen_menu,
					debugger,
					text_box
					]:
					menu.reset_cache()

				old_options = options_menu.buttons.copy()

			elif selected == "Back" or cancel:
				options_menu.buttons = old_options.copy()
				if old_game_state == "pause_menu":
					game_state = "main_game"
					pause = True
				else:
					game_state = old_game_state
					options_menu.reset_cursor()

			# =============== [ OPTIONS GRAPHIC ] ==============

			screen.fill(darkblue)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			options_menu.draw(pixel_size, black_bar)

		# ================= [ TEST ] ===================

		if debug:
			if debug_timer.time_now() > 0.1:
				debug_list = [
					f"fps: {curr_fps()}", 
					f"resolution: {(curr_width, curr_height)}", 
					f"scene: {scene_manager.current_scene}", 
					f"x: {player.pos[0]}",
					f"y: {player.pos[1]}",
					f"px_size: {pixel_size}"
				]
				debug_timer.restart()
			debugger.print_debug(debug_list, black_bar)

		# ================= [ PYGAME STUFF ] ================

		pg.display.update()
		clock_tick(cap_fps, target_fps)
		await asyncio.sleep(0)

	pg.quit()
	exit()

if __name__ == "__main__":
	asyncio.run(main())
