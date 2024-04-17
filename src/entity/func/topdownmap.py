import pygame as pg

def move_map(camera, pixel_size):
	screen_width = camera.tdmap.screen.get_width()
	screen_height = camera.tdmap.screen.get_height()

	if camera.follow_player_x_left and camera.follow_player_x_right:
		camera.tdmap.x = -camera.player.pos[0] * pixel_size + screen_width/2

	if camera.follow_player_y_up and camera.follow_player_y_down:
		camera.tdmap.y = -camera.player.pos[1] * pixel_size + screen_height/2

	if not camera.follow_player_x_left:
		if camera.player.pos[0] < camera.stop_follow_player_left_at_pos_x:
			camera.tdmap.x = -camera.stop_follow_player_left_at_pos_x*pixel_size + pixel_size + screen_width/2

	elif not camera.follow_player_x_right:
		if camera.player.pos[0] > camera.stop_follow_player_right_at_pos_x:
			camera.tdmap.x = -camera.stop_follow_player_right_at_pos_x*pixel_size + pixel_size + screen_width/2

	if not camera.follow_player_y_up:
		if camera.player.pos[1] < camera.stop_follow_player_up_at_pos_y:
			camera.tdmap.y = (-camera.stop_follow_player_up_at_pos_y)*pixel_size - pixel_size + screen_height/2

	elif not camera.follow_player_y_down:
		if camera.player.pos[1] > camera.stop_follow_player_down_at_pos_y:
			camera.tdmap.y = (-camera.stop_follow_player_down_at_pos_y)*pixel_size - pixel_size + screen_height/2


def correct_all_map_rect(tdmap, pixel_size):
	tile_size = pixel_size*16
	map_offset = tile_size/2
	transformed_rects = [(pg.Rect(rect.x * pixel_size + tdmap.x + map_offset,
		rect.y * pixel_size + tdmap.y + map_offset,
		rect.width * pixel_size,
		rect.height * pixel_size), color) for rect, color in tdmap.rects]
	return transformed_rects