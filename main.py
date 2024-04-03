import pygame as pg
pg.mixer.init()
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
import sys
import asyncio
import time
from variable.settings import clock_tick, current_fps,\
 load_settings, default_screen_width, \
 update_size, black, green, red, blue
from func.event_checker import check_event
from func.drawer import draw_black_bar
from func.debug import print_debug
from object.player import Player
from object.map import TopDownMap
from object.timer import Timer
from math import ceil

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

async def main():

	cap_fps = False
	run = True
	debug = True
	print_list = ""
	screen, black_bar = load_settings()
	current_width, current_height, pixel_size = update_size([screen.get_width(), screen.get_height()])
	new_size = (current_width, current_height)
	aspect_ratio = current_width/current_height

	player = Player()
	
	player.add_rect(pg.Rect(0, -8, 16, 8), black)

	top_down_map = TopDownMap()

	top_down_map.add_rect(pg.Rect(0, 0, 128, 112), black)
	top_down_map.add_rect(pg.Rect(128, 0, 128, 112), blue)

	milli_sec_timer = Timer()
	milli_sec_timer.start()

	prev_time = time.time()
	while run:
		# =================== [ DELTA TIME ] ===================

		dt = time.time() - prev_time
		prev_time = time.time()

		# ====================== [ LOGIC ] ======================

		player.update(dt, pixel_size, screen)
		top_down_map.update(pixel_size, player, screen)

		# ===================== [ GRAPHIC ] =====================

		screen.fill(green)
		top_down_map.draw(screen)
		player.draw(screen)
		if black_bar:
			draw_black_bar(current_width, current_height, aspect_ratio)

		# ====================== [ DEBUG ] ======================

		if debug:
			if milli_sec_timer.time_now()>0.1:
				print_list = [current_fps(), 
				f"resolution: {(current_width, current_height)}", 
				f"player_lo: {[player.location[0], player.location[1]]}",
				f"pixel_size: {pixel_size}"]
				milli_sec_timer.restart()
			print_debug(print_list)

		# ====================== [ EVENT ] ======================

		run, new_size = check_event(pg.event.get(), new_size)

		# ====================== [ RESIZE ] ======================

		is_resize = [current_width, current_height] != new_size
		if is_resize:
			current_width, current_height, pixel_size = update_size(new_size)

		# =================== [ PYGAME STUFF ] ===================

		pg.display.update()
		clock_tick(cap_fps)
		await asyncio.sleep(0)

	pg.quit()
	sys.exit()


if __name__ == "__main__":
	asyncio.run(main())
