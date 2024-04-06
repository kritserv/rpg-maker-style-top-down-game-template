import pygame as pg

def toggle_full_screen(new_size, default_screen_size):
	if not pg.display.is_fullscreen():
		screen = pg.display.set_mode(new_size, pg.FULLSCREEN)
	else:
		screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
	return screen