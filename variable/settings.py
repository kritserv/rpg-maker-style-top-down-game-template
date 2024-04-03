import pygame as pg
import json
from object.timer import Timer
from math import ceil

clock = pg.time.Clock()

timer_1_sec = Timer()
timer_1_sec.start()

def clock_tick(cap_fps):
	if cap_fps:
		clock.tick(60)
	else:
		clock.tick()

def current_fps():
	get_fps = str(clock.get_fps() // 0.1 / 10)
	return f"fps: {get_fps}"

default_screen_width = 480
default_screen_height = 432

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

def update_size(new_size):
	current_width, current_height = new_size[0], new_size[1]
	pixel_size = ceil(current_width/default_screen_width)
	return current_width, current_height, pixel_size

debug_font = pg.font.SysFont(None, 22)

red = pg.Color(255, 127, 127)
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
green = pg.Color(127, 255, 127)
blue = pg.Color(127, 127, 255)