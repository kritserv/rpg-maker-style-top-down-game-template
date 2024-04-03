import pygame as pg
from variable.settings import screen, black

def blit_text(text, font, col, x_y_pos):
	text_image = font.render(text, True, col)
	screen.blit(text_image, x_y_pos)

def draw_black_bar(current_width, current_height, aspect_ratio):
	if current_width/current_height>aspect_ratio:
		bar_width = (current_width - current_height * (aspect_ratio)) / 2
		pg.draw.rect(screen, black, (0, 0, bar_width, current_height))
		pg.draw.rect(screen, black, (current_width - bar_width+1, 0, bar_width, current_height))