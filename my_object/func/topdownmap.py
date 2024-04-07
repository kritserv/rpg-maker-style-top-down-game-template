import pygame as pg

def move_map(camera, pixel_size):
	if camera.follow_player_x_left and camera.follow_player_x_right:
		camera.tdmap.x = -camera.player.pos[0] * pixel_size + camera.tdmap.screen.get_width()/2

	elif not camera.follow_player_x_left:
		if camera.player.pos[0] < camera.stop_follow_player_x_at_pos_left:
			camera.tdmap.x = -camera.stop_follow_player_x_at_pos_left*pixel_size + pixel_size + camera.tdmap.screen.get_width()/2

	elif not camera.follow_player_x_right:
		if camera.player.pos[0] > camera.stop_follow_player_x_at_pos_right:
			camera.tdmap.x = -camera.stop_follow_player_x_at_pos_right*pixel_size + pixel_size + camera.tdmap.screen.get_width()/2

	if camera.follow_player_y:
		camera.tdmap.y = -camera.player.pos[1] * pixel_size + camera.tdmap.screen.get_height()/2
	else:
		camera.tdmap.y = pixel_size + camera.tdmap.screen.get_height()/2

def correct_all_map_rect(tdmap, pixel_size):
	tile_size = pixel_size*16
	map_offset = tile_size/2
	transformed_rects = [(pg.Rect(rect.x * pixel_size + tdmap.x + map_offset,
		rect.y * pixel_size + tdmap.y + map_offset,
		rect.width * pixel_size,
		rect.height * pixel_size), color) for rect, color in tdmap.rects]
	return transformed_rects
