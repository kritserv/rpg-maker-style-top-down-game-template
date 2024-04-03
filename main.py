import pygame as pg
pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
import sys
import asyncio
import time
from variable.settings import clock_tick, curr_fps,\
 load_settings, default_screen_width, default_screen_height, \
 update_size, black, green, red, blue
from func.event_checker import check_event
from func.debug import print_debug
from object.player import Player
from object.map import TopDownMap
from object.timer import Timer
from object.blackbar import BlackBar

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

async def main():

	cap_fps = False
	run = True
	debug = True
	print_list = ""

	screen, black_bar_is_set = load_settings()
	black_bar = BlackBar(screen, black_bar_is_set)
	curr_width, curr_height, pixel_size = update_size(
		[screen.get_width(), 
		screen.get_height()])
	ratio = default_screen_width/default_screen_height
	new_size = (curr_width, curr_height)

	obstacles = [
		(pg.Rect(-80, -112, 112, 64), black), (pg.Rect(80, -112, 112, 64), red),
		(pg.Rect(-80, 32, 112, 64), blue), (pg.Rect(80, 32, 112, 64), red)]

	player = Player(screen, cap_fps)
	
	player.add_rect(pg.Rect(0, -8, 16, 8), black)

	player.resize(pixel_size)

	player.obstacles = [ob for ob, color in obstacles]
	player.calculate_obstacles_location()

	top_down_map = TopDownMap(screen)


	top_down_map.resize(pixel_size, player)

	top_down_map.rects = [ob for ob in obstacles]

	milli_sec_timer = Timer()
	milli_sec_timer.start()

	prev_time = time.time()
	while run:
		# =================== [ DELTA TIME ] ===================

		dt = time.time() - prev_time
		prev_time = time.time()

		# ====================== [ LOGIC ] ======================

		player.update(dt, pixel_size)
		top_down_map.update(pixel_size, player)

		# ====================== [ GRAPHIC ] =====================

		curr_width, curr_height, pixel_size = update_size(new_size)
		player.resize(pixel_size)
		top_down_map.resize(pixel_size, player)

		screen.fill(green)
		top_down_map.draw()
		player.draw()
		black_bar.draw_if_set(curr_width, curr_height, ratio)

		# ====================== [ DEBUG ] ======================

		if debug:
			if milli_sec_timer.time_now()>0.1:
				print_list = [curr_fps(), 
				f"resolution: {(curr_width, curr_height)}", 
				f"player_lo: {player.location}"]
				milli_sec_timer.restart()
			print_debug(print_list)

		# ====================== [ EVENT ] ======================

		run, new_size = check_event(pg.event.get(), new_size)

		# =================== [ PYGAME STUFF ] ===================

		pg.display.update()
		clock_tick(cap_fps)
		await asyncio.sleep(0)

	pg.quit()
	sys.exit()


if __name__ == "__main__":
	asyncio.run(main())
