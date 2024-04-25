import pygame as pg

def check_quit_game(event, quit, keydown):
	run = True
	if quit:
		run = False
	if keydown:
		if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Q
			run = False
		elif event.key == pg.K_F4 and pg.key.get_mods() & pg.KMOD_ALT:  # Alt + F4
			run = False

	return run

def check_debug_mode(event, debug):
	if event.key == pg.K_F3:
		debug = not debug

	return debug

def check_window_resize(event, new_size, resize):
	if resize:
		new_size = event.dict["size"]

	return new_size

def check_full_screen_toggle(event):
	full_screen_toggle = False
	if event.key == pg.K_F11:
		full_screen_toggle = True

	return full_screen_toggle

full_screen_size = pg.display.get_desktop_sizes()[0]

def check_interact(event, keydown, keyup):
	interact = False
	if keydown:
		if event.key == pg.K_RETURN:
			interact = True
	elif keyup:
		if event.key == pg.K_z or event.key == pg.K_SPACE:
			interact = True

	return interact

def check_cancel(event, keydown, keyup):
	cancel = False
	if keydown:
		if event.key == pg.K_ESCAPE:
			cancel = True
	elif keyup:
		if event.key == pg.K_x or event.key == pg.K_KP0:
			cancel = True

	return cancel

def check_pause_toggle(event, keydown, keyup):
	return check_cancel(event, keydown, keyup)

def check_type(event):
	keydown, keyup, quit, resize = False, False, False, False
	if event.type == pg.KEYDOWN:
		keydown = True
	elif event.type == pg.KEYUP:
		keyup = True
	elif event.type == pg.QUIT:
		quit = True
	elif event.type == pg.VIDEORESIZE:
		resize = True
	return keydown, keyup, quit, resize

def check_pygame_event(all_event, new_size, debug):
	run = True
	full_screen_toggle = False
	pause_toggle = False
	interact = False
	for event in all_event:

		keydown, keyup, quit, resize = check_type(event)

		new_size = check_window_resize(event, new_size, resize)
		run = check_quit_game(event, quit, keydown)
		interact = check_interact(event, keydown, keyup)
		pause_toggle = check_pause_toggle(event, keydown, keyup)

		if keydown:
			debug = check_debug_mode(event, debug)
			full_screen_toggle = check_full_screen_toggle(event)

		if full_screen_toggle:
			new_size = full_screen_size

	return run, new_size, debug, full_screen_toggle, pause_toggle, interact