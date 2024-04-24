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

def check_debug_mode(event, debug):
	if event.type == pg.KEYDOWN:
		if event.key == pg.K_F3:
			debug = not debug

	return debug

def check_window_resize(event, new_size):
	if event.type == pg.VIDEORESIZE:
		new_size = event.dict['size']

	return new_size

def check_full_screen_toggle(event):
	full_screen_toggle = False
	if event.type == pg.KEYDOWN:
		if event.key == pg.K_F11:
			full_screen_toggle = True

	return full_screen_toggle

full_screen_size = pg.display.get_desktop_sizes()[0]

def check_pause_toggle(event):
	pause_toggle = False
	if event.type == pg.KEYDOWN:
		if event.key == pg.K_ESCAPE:
			pause_toggle = True

	return pause_toggle

def check_interact(event):
	interact = False
	if event.type == pg.KEYDOWN:
		if event.key == pg.K_RETURN:
			interact = True
	elif event.type == pg.KEYUP:
		if event.key == pg.K_z:
			interact = True

	return interact

def check_pygame_event(all_event, new_size, debug):
	run = True
	full_screen_toggle = False
	pause_toggle = False
	interact = False
	for event in all_event:
		run = check_quit_game(event)
		new_size = check_window_resize(event, new_size)
		debug = check_debug_mode(event, debug)
		pause_toggle = check_pause_toggle(event)
		full_screen_toggle = check_full_screen_toggle(event)
		interact = check_interact(event)
		if full_screen_toggle:
			new_size = full_screen_size

	return run, new_size, debug, full_screen_toggle, pause_toggle, interact