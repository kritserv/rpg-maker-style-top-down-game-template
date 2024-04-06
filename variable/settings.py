import pygame as pg
import json
from math import ceil, floor

clock = pg.time.Clock()

def clock_tick(cap_fps):
	if cap_fps:
		clock.tick(60)
	else:
		clock.tick()

def curr_fps():
	get_fps = str(clock.get_fps() // 0.1 / 10)
	return f"fps: {get_fps}"

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

def round_pixel(num):
	num_floor = floor(num)
	num_ceil = ceil(num)
	num_frac = num - num_floor

	if 0.3 <= num_frac <= 0.7:
		return 0.5 + num_floor
	else:
		return num_floor if num_frac < 0.5 else num_ceil

def limit_pixel(pixel_size):
	if pixel_size > 3.5:
		pixel_size = 3.5
	return pixel_size
	
def update_size(new_size):
	curr_width, curr_height = new_size[0], new_size[1]
	pixel_size = curr_width/default_screen_width
	pixel_size *= native_screen_multiplier
	pixel_size = round_pixel(pixel_size)
	pixel_size = limit_pixel(pixel_size)
	return curr_width, curr_height, pixel_size

red = pg.Color("crimson")
black = pg.Color("grey0")
white = pg.Color("grey100")
green = pg.Color("palegreen3")
blue = pg.Color("royalblue2")

debug_font = pg.font.Font("asset/font/PixeloidSans-mLxMm.ttf", 14)
