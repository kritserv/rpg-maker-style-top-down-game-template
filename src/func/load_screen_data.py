import pygame as pg
from src.variable import default_screen_size
from .load_json_file import json_loader

def load_screen_from_json():
	full_screen_size = pg.display.get_desktop_sizes()[0]
	black_bar = False
	cap_fps = False

	json_load = json_loader("user_data/settings.json")
	full_screen = json_load["fullscreen"]
	blackbar = json_load["blackbar"]
	capfps = json_load["capfps"]
	target_fps = json_load["capfps_at"]
	
	if full_screen == "True":
		screen = pg.display.set_mode(full_screen_size, pg.FULLSCREEN)
		full_screen = True
	else:
		screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
		full_screen = False
	if blackbar == "True":
		black_bar = True
	if capfps == "True":
		cap_fps = True
	return screen, full_screen, black_bar, cap_fps, target_fps

