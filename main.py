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
	toggle_full_screen, load_scene_from_json_data
from func import check_event, print_debug
from my_object import Player, TopDownMap, Camera, \
	BlackBar, Timer

pg.display.set_caption("game_title")
pg.display.set_icon(pg.image.load("asset/img/icon.png"))

def change_scene(player, x, y, top_down_map, scene_dict, new_scene_name):
	player.obs = [ob for ob, color in scene_dict[new_scene_name]]
	player.calculate_obs_pos()
	player.pos = [x, y]
	player.finish_pos = [x, y]
	top_down_map.rects = [ob for ob in scene_dict[new_scene_name]]
	top_down_map.current_scene = new_scene_name

def change_camera_stop_position(camera, stop_left, stop_right, stop_up, stop_down):
	camera.stop_follow_player_left_at_pos_x = stop_left
	camera.stop_follow_player_right_at_pos_x = stop_right
	camera.stop_follow_player_up_at_pos_y = stop_up
	camera.stop_follow_player_down_at_pos_y = stop_down

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

	scene_data = load_scene_from_json_data()

	scene = {
		"openworld": scene_data["house1"] + scene_data["house2"] + scene_data["house3"] + scene_data["openworld_border"],
		"inner_house1": scene_data["inner_house_border"],
		"inner_house2": scene_data["inner_house_border"],
		"inner_house3": scene_data["inner_house_border"],
	}

	start_scene_name = "openworld"

	player = Player(screen)
	
	player.rects = [(pg.Rect(0, 0, 16, 16), red), 
		(pg.Rect(0, -8, 16, 8), red)
	]

	player.resize(pixel_size)
	player.obs = [ob for ob, color in scene[start_scene_name]]
	player.calculate_obs_pos()
	player.pos = [-64, 0]

	top_down_map = TopDownMap(screen, start_scene_name)
	top_down_map.rects = [ob for ob in scene[start_scene_name]]
	top_down_map.resize(pixel_size, player)

	camera = Camera(player, top_down_map)
	change_camera_stop_position(camera, -144, 144, -160, 160)

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

		if top_down_map.current_scene == "openworld" and player.pos == [-80, -48]:
			change_scene(player, 0, 48, top_down_map, scene, "inner_house1")
			change_camera_stop_position(camera, -48, 48, -64, 16)

		if top_down_map.current_scene == "inner_house1" and player.pos == [0, 64]:
			change_scene(player, -80, -16, top_down_map, scene, "openworld")
			change_camera_stop_position(camera, -144, 144, -160, 160)

		if top_down_map.current_scene == "openworld" and player.pos == [80, -48]:
			change_scene(player, 0, 48, top_down_map, scene, "inner_house2")
			change_camera_stop_position(camera, -48, 48, -64, 16)

		if top_down_map.current_scene == "inner_house2" and player.pos == [0, 64]:
			change_scene(player, 80, -16, top_down_map, scene, "openworld")
			change_camera_stop_position(camera, -144, 144, -160, 160)

		if top_down_map.current_scene == "openworld" and player.pos == [-80, 96]:
			change_scene(player, 0, 48, top_down_map, scene, "inner_house3")
			change_camera_stop_position(camera, -48, 48, -64, 16)

		if top_down_map.current_scene == "inner_house3" and player.pos == [0, 64]:
			change_scene(player, -80, 128, top_down_map, scene, "openworld")
			change_camera_stop_position(camera, -144, 144, -160, 160)

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
					f"scene: {top_down_map.current_scene}", 
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
