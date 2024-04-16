import pygame as pg

native_screen_multiplier = 4

default_screen_width = 240 * native_screen_multiplier
default_screen_height = 160 * native_screen_multiplier

default_screen_size = (default_screen_width, default_screen_height)

screen = pg.display.set_mode(default_screen_size, pg.RESIZABLE)