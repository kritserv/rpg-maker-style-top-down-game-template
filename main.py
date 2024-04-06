import pygame as pg
pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
import sys
import asyncio
import time
from variable import clock_tick, curr_fps,\
	load_settings, default_screen_width, \
	default_screen_height, default_screen_size, \
	update_size, black, green, red, blue
from func import check_event, print_debug, \
	toggle_full_screen
from my_object import Player, TopDownMap, Timer, \
	BlackBar

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

async def main():

	run = True
	cap_fps = False
	debug = False
	debug_list = [""]
	full_screen_toggle = False

	screen, black_bar_is_set = load_settings()
	black_bar = BlackBar(screen, black_bar_is_set)
	curr_width, curr_height, pixel_size = update_size(
		[screen.get_width(), 
		screen.get_height()])
	ratio = default_screen_width/default_screen_height
	new_size = (curr_width, curr_height)

	obstacles = [
		(pg.Rect(-80, -112, 112, 64), blue), 
		(pg.Rect(80, -112, 112, 64), red),
		(pg.Rect(-80, 32, 112, 64), blue), 
		(pg.Rect(80, 32, 112, 64), red)
		]

	player = Player(screen)
	
	player.rects = [(pg.Rect(0, 0, 16, 16), red), 
		(pg.Rect(0, -8, 16, 8), black)
	]

	player.resize(pixel_size)

	player.obs = [ob for ob, color in obstacles]

	player.calculate_obs_pos()

	top_down_map = TopDownMap(screen)

	top_down_map.rects = [ob for ob in obstacles]

	top_down_map.resize(pixel_size, player)

	debug_timer = Timer()
	debug_timer.start()

	prev_time = time.time()
	while run:
		# =================== [ DELTA TIME ] ===================

		dt = time.time() - prev_time
		prev_time = time.time()

		# ====================== [ LOGIC ] ======================

		player.update(dt, pixel_size)
		top_down_map.update(pixel_size, player)

		# ====================== [ GRAPHIC ] =====================

		if full_screen_toggle:
			full_screen_toggle = False
			screen = toggle_full_screen(
				new_size, default_screen_size
			)

		curr_width, curr_height, pixel_size = update_size(
			new_size)
		player.resize(pixel_size)
		top_down_map.resize(pixel_size, player)

		screen.fill(green)
		top_down_map.draw()
		player.draw()
		black_bar.draw_if_set(curr_width, curr_height, ratio)

		# ====================== [ TEST ] ======================

		if debug:
			if debug_timer.time_now()>0.1:
				debug_list = [
					curr_fps(), 
					f"resolution: {(curr_width, curr_height)}", 
					f"x: {player.pos[0]}", 
					f"y: {player.pos[1]}"
				]
				debug_timer.restart()
			print_debug(debug_list)

		# ====================== [ EVENT ] ======================

		run, new_size, debug, full_screen_toggle = check_event(
			pg.event.get(), new_size, debug
			)

		# =================== [ PYGAME STUFF ] ===================

		pg.display.update()
		clock_tick(cap_fps)
		await asyncio.sleep(0)

	pg.quit()
	sys.exit()

if __name__ == "__main__":
	asyncio.run(main())
