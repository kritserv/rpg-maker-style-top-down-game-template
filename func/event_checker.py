import pygame as pg

def check_quit_game(event):
	run = True
	if event.type == pg.QUIT:
		run = False
	elif event.type == pg.KEYDOWN:
		if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL:
			run = False
		elif event.key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
			run = False
	else:
		pass

	return run

def check_window_resize(event, new_size):
	if event.type == pg.VIDEORESIZE:
		new_size = event.dict['size']

	return new_size

def check_event(all_event, new_size):
	run = True
	for event in all_event:
		run = check_quit_game(event)
		new_size = check_window_resize(event, new_size)

	return run, new_size