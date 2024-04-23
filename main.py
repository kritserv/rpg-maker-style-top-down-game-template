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
	Player, TopDownMap, Camera, BlackBar, \
	Timer, SceneManager, Event, Cursor

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

async def main():
	run = True
	web_export = False
	debug = True
	debug_list = [""]
	full_screen_toggle = False

	screen, black_bar_is_set, cap_fps = load_screen_from_json()
	black_bar = BlackBar(screen, black_bar_is_set)
	curr_width, curr_height, pixel_size = update_size(
		[screen.get_width(), 
		screen.get_height()]
		)
	ratio = default_screen_width/default_screen_height
	new_size = (curr_width, curr_height)

	low_fps_mode, high_fps_mode = 0, 1
	if cap_fps or web_export:
		low_fps_mode, high_fps_mode = 0.015, 0

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

	event.trigger(start_event["effect"])

	cursor = Cursor(screen)
	cursor.obs = [[-16, -32, 16, 16], [-16, 48, 16, 16]]
	cursor.calculate_obs_pos()

	debug_timer = Timer()
	debug_timer.start()

	game_state = "title_menu"

	prev_time = time()
	
	plus_value = 10
	while run:
		# ================== [ DELTA TIME ] ==================

		dt = time() - prev_time
		dt *= high_fps_mode
		dt += low_fps_mode
		prev_time = time()

		key = pg.key.get_pressed()
		if game_state == "title_menu":

			# ================== [ TITLE LOGIC ] ================

			cursor.update(dt, key)
			if key[pg.K_RETURN]:
				if cursor.pos[1] == 0:
					game_state = "main_game"
				elif cursor.pos[1] == 16:
					game_state = "main_game"
				elif cursor.pos[1] == 32:
					pass
				elif cursor.pos[1] == 48:
					break
			if key[pg.K_UP] and cursor.pos[1] == 0:
					cursor.pos[1] = 48 + plus_value
			elif key[pg.K_DOWN] and cursor.pos[1] == 48:
					cursor.pos[1] = 0 - plus_value

			# ================= [ TITLE GRAPHIC ] ================

			if full_screen_toggle:
				full_screen_toggle = False
				screen = toggle_full_screen(
					new_size, default_screen_size
				)

			curr_width, curr_height, pixel_size = update_size(
				new_size
				)
			cursor.resize(pixel_size)

			screen.fill(black)
			cursor.draw(pixel_size)
			black_bar.draw_if_set(curr_width, curr_height, ratio)

			# ================= [ TEST ] ===================

			if debug:
				if debug_timer.time_now() > 0.1:
					debug_list = [
						f"fps: {curr_fps()}", 
						f"resolution: {(curr_width, curr_height)}", 
						f"x: {cursor.pos[0]}",
						f"y: {cursor.pos[1]}",
						f"px_size: {pixel_size}"
					]
					debug_timer.restart()
				print_debug(debug_list)

		elif game_state == "main_game":

			# ================= [ MAIN LOGIC ] =================

			player.update(dt, key)
			camera.update(pixel_size)
			event.update()

			# ================= [ MAIN GRAPHIC ] ===============

			if full_screen_toggle:
				full_screen_toggle = False
				screen = toggle_full_screen(
					new_size, default_screen_size
				)

			curr_width, curr_height, pixel_size = update_size(
				new_size
				)
			player.resize(pixel_size)
			top_down_map.resize(pixel_size, player)

			screen.fill(black)
			camera.draw(pixel_size, player, top_down_map)
			black_bar.draw_if_set(curr_width, curr_height, ratio)

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

		# ================= [ PYGAME STUFF ] ================

		run, new_size, debug, full_screen_toggle = check_pygame_event(
			pg.event.get(), new_size, debug
			)
		pg.display.update()
		clock_tick(cap_fps)
		await asyncio.sleep(0)

	pg.quit()
	exit()

if __name__ == "__main__":
	asyncio.run(main())
