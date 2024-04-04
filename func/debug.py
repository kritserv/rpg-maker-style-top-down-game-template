import pygame as pg
from .drawer import blit_text
from variable.settings import screen, debug_font, white, black

def print_debug(print_list):
	y_pos = 5
	debug_background = pg.Surface((300, len(print_list) * 23))
	debug_background.set_alpha(150)
	debug_background.fill(black)
	screen.blit(debug_background, (0, 0))
	for text in print_list:
		if not isinstance(text, str):
			text = str(text)
		blit_text(text, debug_font, white, (10, y_pos))
		y_pos += 20
