import pygame as pg
import json
from src.variable import default_screen_size

def load_screen_from_json():
	full_screen_size = pg.display.get_desktop_sizes()[0]
	black_bar = False
	cap_fps = False
	with open("user_data/settings.json") as f:
		json_load = json.load(f)
		full_screen = json_load["fullscreen"]
		blackbar = json_load["blackbar"]
		capfps = json_load["capfps"]
		f.close()
	if full_screen == "True":
		screen = pg.display.set_mode(full_screen_size, pg.FULLSCREEN)
	else:
		screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)
	if blackbar == "True":
		black_bar = True
	if capfps == "True":
		cap_fps = True
	return screen, black_bar, cap_fps

