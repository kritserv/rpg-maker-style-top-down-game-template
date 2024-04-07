import pygame as pg
import json
from math import ceil, floor

native_screen_multiplier = 4

default_screen_width = 240 * native_screen_multiplier
default_screen_height = 160 * native_screen_multiplier

default_screen_size = (default_screen_width, default_screen_height)

screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)

def load_settings():
	full_screen_size = pg.display.get_desktop_sizes()[0]
	black_bar = False
	with open("settings.json") as f:
		json_load = json.load(f)
		full_screen = json_load["fullscreen"]
		blackbar = json_load["blackbar"]
		f.close()
	if full_screen=="True":
		screen = pg.display.set_mode(full_screen_size, pg.FULLSCREEN)
	else:
		screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
	if blackbar=="True":
		black_bar = True
	return screen, black_bar

def toggle_full_screen(new_size, default_screen_size):
	if not pg.display.is_fullscreen():
		screen = pg.display.set_mode(new_size, pg.FULLSCREEN)
	else:
		screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
	return screen

def round_pixel(num):
	num_floor = floor(num)
	num_ceil = ceil(num)
	num_frac = num - num_floor

	if 0.3 <= num_frac <= 0.7:
		return 0.5 + num_floor
	else:
		return num_floor if num_frac < 0.5 else num_ceil

def limit_pixel(pixel_size):
	pixel_size -= 2

	if pixel_size > 11:
		pixel_size = 4
	elif 4 < pixel_size <= 11:
		pixel_size = 3
	elif 1 < pixel_size <= 1.5:
		pixel_size = 1.5
	elif pixel_size <= 1:
		pixel_size = 1

	return pixel_size

	
def update_size(new_size):
	curr_width, curr_height = new_size[0], new_size[1]
	pixel_size = curr_width/default_screen_width
	pixel_size *= native_screen_multiplier
	pixel_size = round_pixel(pixel_size)
	pixel_size = limit_pixel(pixel_size)
	return curr_width, curr_height, pixel_size