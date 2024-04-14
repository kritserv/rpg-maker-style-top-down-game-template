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
	update_size, black, green, red, blue, \
	toggle_full_screen
from func import check_event, print_debug
from my_object import Player, TopDownMap, Camera, \
	BlackBar, Timer

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

def create_house(x, y, color):
    house = [
        (pg.Rect(x, y, 48, 64), color),
        (pg.Rect(x+48, y, 16, 48), color),
        (pg.Rect(x+64, y, 48, 64), color)
    ]
    return house
    

async def main():

	run = True
	cap_fps = False
	debug = True
	debug_list = [""]
	full_screen_toggle = False

	screen, black_bar_is_set = load_settings()
	black_bar = BlackBar(screen, black_bar_is_set)
	curr_width, curr_height, pixel_size = update_size(
		[screen.get_width(), 
		screen.get_height()])
	ratio = default_screen_width/default_screen_height
	new_size = (curr_width, curr_height)
	
	house1 = create_house(-144, -112, blue)
	house2 = create_house(16, -112, blue)
	house3 = create_house(-144, 32, blue)
	borders = [
	    (pg.Rect(-208, -240, 384, 16), black),
	    (pg.Rect(-208, 240, 400, 16), black),
	    (pg.Rect(-208, -224, 16, 464), black),
	    (pg.Rect(176, -240, 16, 480), black)
	]

	obstacles = house1 + house2 + house3 + borders


	player = Player(screen)
	
	player.rects = [(pg.Rect(0, 0, 16, 16), red), 
		(pg.Rect(0, -8, 16, 8), red)
	]

	player.resize(pixel_size)

	player.obs = [ob for ob, color in obstacles]

	player.calculate_obs_pos()

	player.pos = [-64, 0]

	top_down_map = TopDownMap(screen)

	top_down_map.rects = [ob for ob in obstacles]

	top_down_map.resize(pixel_size, player)

	camera = Camera(player, top_down_map)
	camera.stop_follow_player_left_at_pos_x = -144
	camera.stop_follow_player_right_at_pos_x = 144
	camera.stop_follow_player_up_at_pos_y = -160
	camera.stop_follow_player_down_at_pos_y = 160

	debug_timer = Timer()
	debug_timer.start()

	prev_time = time.time()
	while run:
		# =================== [ DELTA TIME ] ===================

		dt = time.time() - prev_time
		prev_time = time.time()

		# ====================== [ LOGIC ] ======================

		player.update(dt)
		camera.update(pixel_size)

		if player.pos == [-80, -48]:
			print("enter house 1")
			player.pos = [-80, -496]
			camera.stop_follow_player_left_at_pos_x = -80
			camera.stop_follow_player_right_at_pos_x = -80
			camera.stop_follow_player_up_at_pos_y = -624
			camera.stop_follow_player_down_at_pos_y = -624

		if player.pos[0] == -80 and -448 >= player.pos[1] >= -495:
			print("exit house 1")
			camera.stop_follow_player_left_at_pos_x = -144
			camera.stop_follow_player_right_at_pos_x = 144
			camera.stop_follow_player_up_at_pos_y = -160
			camera.stop_follow_player_down_at_pos_y = 160
			player.pos = [-80, -16]

		if player.pos == [80, -48]:
			print("enter house 2")
			player.pos = [0, 0]

		if player.pos == [-80, 96]:
			print("enter house 3")
			player.pos = [0, 0]

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
		camera.draw(pixel_size, player, top_down_map)
		black_bar.draw_if_set(curr_width, curr_height, ratio)

		# ====================== [ TEST ] ======================

		if debug:
			if debug_timer.time_now()>0.1:
				debug_list = [
					curr_fps(), 
					f"resolution: {(curr_width, curr_height)}", 
					f"x: {player.pos[0]}", 
					f"y: {player.pos[1]}",
					f"px_size: {pixel_size}"
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
