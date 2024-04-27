import pygame as pg

clock = pg.time.Clock()

def clock_tick(cap_fps, target_fps):
	if cap_fps:
		clock.tick(target_fps)
	else:
		clock.tick()

def curr_fps():
	get_fps = str(clock.get_fps() // 0.1 / 10)
	return get_fps