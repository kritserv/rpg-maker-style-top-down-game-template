import pygame as pg

def move_map(tdmap, pixel_size, player):
	tdmap.x = -player.pos[0] * pixel_size + tdmap.screen.get_width()/2
	tdmap.y = -player.pos[1] * pixel_size + tdmap.screen.get_height()/2

def correct_all_map_rect(tdmap, pixel_size):
	tile_size = pixel_size*16
	map_offset = tile_size/2
	transformed_rects = [(pg.Rect(rect.x * pixel_size + tdmap.x + map_offset,
	    rect.y * pixel_size + tdmap.y + map_offset,
	    rect.width * pixel_size,
	    rect.height * pixel_size), color) for rect, color in tdmap.rects]
	return transformed_rects
