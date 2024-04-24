import pygame as pg

clock = pg.time.Clock()

def clock_tick(cap_fps):
	if cap_fps:
		clock.tick(60)
	else:
		clock.tick()

def curr_fps():
	get_fps = str(clock.get_fps() // 0.1 / 10)
	return get_fps

debug_font = pg.font.Font("asset/font/PixeloidSans-mLxMm.ttf", 14)

font_x1 = pg.font.Font("asset/font/PixeloidSans-mLxMm.ttf", 6)
font_x2 = pg.font.Font("asset/font/PixeloidSans-mLxMm.ttf", 12)
font_x3 = pg.font.Font("asset/font/PixeloidSans-mLxMm.ttf", 18)