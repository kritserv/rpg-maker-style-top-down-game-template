import pygame as pg
from variable.settings import screen

def blit_text(text, font, col, x_y_pos):
	text_image = font.render(text, True, col)
	screen.blit(text_image, x_y_pos)