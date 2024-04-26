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
	black, check_pygame_event, \
	print_debug, load_screen_from_json, \
	toggle_full_screen, update_size, \
	load_scene_from_json, load_event_from_json, \
	load_save_from_json, \
	Player, TopDownMap, Camera, BlackBar, \
	Timer, SceneManager, SaveManager, Event, Cursor, Menu

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

async def main():
	run = True
	web_export = False
	debug = False
	debug_list = [""]
	full_screen_toggle = False
	pause = False
	pause_toggle = False

	screen, black_bar_is_set, cap_fps = load_screen_from_json()
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

	scene_manager = SceneManager(
		load_scene_from_json(), player, top_down_map, camera
		)

	event_dict, start_event = load_event_from_json()
	event = Event(
		event_dict, player, scene_manager
		)

	save_manager = SaveManager(load_save_from_json())
	save_manager.save_menu, save_manager.load_menu = Menu(Cursor(screen)), Menu(Cursor(screen))
	save_manager.create_buttons()
	loadable_slot = [f"Load From Slot {i}" for i in range(8)]

	title_screen_menu = Menu(Cursor(screen))
	title_screen_menu.buttons = [
		"Start Game", "Load Game", "Options", "Quit Game"
		]
	title_screen_menu.setup_buttons()

	pause_menu = Menu(Cursor(screen))
	pause_menu.buttons = [
		"Save", "Load", "Back To Title", "Cancel"
		]
	pause_menu.setup_buttons()

	game_state = "title_screen_menu"

	debug_timer = Timer()
	debug_timer.start()

	prev_time = time()
	while run:

		# ================== [ DELTA TIME ] ==================

		dt = time() - prev_time
		prev_time = time()

		# =================== [ GET INPUT ] ===================

		run, \
		new_size, \
		debug, \
		full_screen_toggle, \
		pause_toggle, \
		interact = check_pygame_event(
			pg.event.get(), new_size, debug
			)
		curr_width, curr_height, pixel_size = update_size(
			new_size
			)
		key = pg.key.get_pressed()

		# =============== [ TOGGLE THE TOGGLEABLE ] ===============

		if pause_toggle:
			pause_toggle = False
			pause = not pause

		if full_screen_toggle:
			full_screen_toggle = False
			screen = toggle_full_screen(
				new_size, default_screen_size
			)

		# ================= [ GET GAME STATE ] =================

		if game_state == "title_screen_menu":
			pause = False

			# ================== [ TITLE LOGIC ] ================

			selected = title_screen_menu.update(dt, key, interact)
			if selected == "Start Game":
				event.trigger(start_event["effect"])
				game_state = "main_game"
			elif selected == "Load Game":
				game_state = "load_game_menu"
				pass
			elif selected == "Options":
				# game_state = "options_menu"
				pass
			elif selected == "Quit Game":
				run = False
			else:
				pass

			# ================= [ TITLE GRAPHIC ] ================

			title_screen_menu.resize(pixel_size)

			screen.fill(black)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			title_screen_menu.draw(pixel_size)

			# ================= [ TEST ] ===================

			if debug:
				if debug_timer.time_now() > 0.1:
					debug_list = [
						f"fps: {curr_fps()}", 
						f"resolution: {(curr_width, curr_height)}", 
						f"x: {title_screen_menu.cursor.pos[0]}",
						f"y: {title_screen_menu.cursor.pos[1]}",
						f"px_size: {pixel_size}"
					]
					debug_timer.restart()
				print_debug(debug_list)

		elif game_state == "main_game":

			# ================= [ MAIN LOGIC ] =================

			if not pause:
				player.update(dt, key)
				camera.update(pixel_size)
				event.update()
			else:
				selected = pause_menu.update(dt, key, interact)
				if selected == "Save":
					# game_state = "save_game_menu"
					pass
				elif selected == "Load":
					# game_state = "load_game_menu"
					pass
				elif selected == "Back To Title":
					game_state = "title_screen_menu"
				elif selected == "Cancel":
					if pause == True:
						pause = False
				else:
					pass

			# ================= [ MAIN GRAPHIC ] ===============

			player.resize(pixel_size)
			top_down_map.resize(pixel_size, player)

			screen.fill(black)
			camera.draw(pixel_size, player, top_down_map)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			if pause:
				pause_menu.resize(pixel_size)
				pause_menu.draw(pixel_size)

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
				print_debug(debug_list)

		elif game_state == "load_game_menu":

			# ================ [ LOAD GAME LOGIC ] ==============

			selected = save_manager.load_menu.update(dt, key, interact)
			for i, slot in enumerate(loadable_slot):
				if selected == slot:
					event.trigger(save_manager.save_dict[str(i)]["event"])
					game_state = "main_game"
			if selected == "Cancel":
				game_state = "title_screen_menu"

			# =============== [ LOAD GAME GRAPHIC ] ==============

			save_manager.load_menu.resize(pixel_size)

			screen.fill(black)
			black_bar.draw_if_set(curr_width, curr_height, ratio)
			save_manager.load_menu.draw(pixel_size)

			# ================= [ TEST ] ===================

			if debug:
				if debug_timer.time_now() > 0.1:
					debug_list = [
						f"fps: {curr_fps()}", 
						f"resolution: {(curr_width, curr_height)}", 
						f"x: {save_manager.load_menu.cursor.pos[0]}",
						f"y: {save_manager.load_menu.cursor.pos[1]}",
						f"px_size: {pixel_size}"
					]
					debug_timer.restart()
				print_debug(debug_list)

		# ================= [ PYGAME STUFF ] ================

		pg.display.update()
		clock_tick(cap_fps)
		await asyncio.sleep(0)

	pg.quit()
	exit()

if __name__ == "__main__":
	asyncio.run(main())
