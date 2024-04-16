import pygame as pg
from variable import default_screen_size, native_screen_multiplier, default_screen_width

def toggle_full_screen(new_size, default_screen_size):
	if not pg.display.is_fullscreen():
		screen = pg.display.set_mode(new_size, pg.FULLSCREEN)
	else:
		screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
	return screen

def limit_pixel(pixel_size):
	pixel_size -= 2

	if pixel_size >= 3:
		return 3

	if pixel_size <= 1:
	 	return 1

	return pixel_size
	
def update_size(new_size):
	curr_width, curr_height = new_size[0], new_size[1]
	pixel_size = curr_width/default_screen_width
	pixel_size = round(pixel_size*native_screen_multiplier)
	pixel_size = limit_pixel(pixel_size)
	return curr_width, curr_height, pixel_size