import pygame as pg
from math import floor, ceil

def correct_all_rect(player, pixel_size):
	transformed_rects = [(pg.Rect(rect.x * pixel_size + player.top_left_x,
	    rect.y * pixel_size + player.top_left_y,
	    rect.width * pixel_size,
	    rect.height * pixel_size), color) for rect, color in player.rects]
	return transformed_rects

def resize_pixel(player, pixel_size):
	screen_width, screen_height = player.screen.get_width(), player.screen.get_height()
	player.x, player.y = screen_width/2, screen_height/2
	player.width, player.height = player.original_width * pixel_size, player.original_height * pixel_size
	player.top_left_x, player.top_left_y = player.x - player.width/2, player.y - player.height/2
	
def calculate_obs_position(ob_list):
	plus_value = 10
	calculated_obs = []
	for ob in ob_list:
		ob_values = {
			"left": [ob[2] + ob[0] + 16 - plus_value, ob[2] + ob[0] + 32 - plus_value, ob[1] + 16, ob[3] + ob[1]],
			"right": [ob[0] - plus_value, ob[0] + 16 - plus_value, ob[1] + 16, ob[3] + ob[1]],
			"up": [ob[0] + 16, ob[2] + ob[0], ob[3] + 16 - plus_value + ob[1], ob[3] + 32 - plus_value + ob[1]],
			"down": [ob[0] + 16, ob[2] + ob[0], ob[1] - plus_value, ob[1] + 16]
		}
		calculated_obs.append(ob_values)
	return calculated_obs

def ob_is_in_direction(player, direction):
	for ob in player.obs:
		if (ob[direction][0] <= player.pos[0] <= ob[direction][1]) and (ob[direction][2] <= player.pos[1] <= ob[direction][3]):
			return True
	return False
	
def move_left_get_obstruct(player):
    return ob_is_in_direction(player, "left")

def move_right_get_obstruct(player):
    return ob_is_in_direction(player, "right")

def move_up_get_obstruct(player):
    return ob_is_in_direction(player, "up")

def move_down_get_obstruct(player):
    return ob_is_in_direction(player, "down")
		
def calculate_movement(player, key):
    dx, dy = 0, 0
    player.key_presed = False
    
    if key[pg.K_LEFT] or key[pg.K_RIGHT]:
        if player.finished_y_move:
            if key[pg.K_LEFT]:
                if not move_left_get_obstruct(player):
            	    dx = -1
            elif key[pg.K_RIGHT]:
                if not move_right_get_obstruct(player):
            	    dx = 1
            if dx != 0:
            	player.last_dx = dx
            	player.key_presed = True
            	player.finished_x_move = False
    elif key[pg.K_UP] or key[pg.K_DOWN]:
        if player.finished_x_move:
            if key[pg.K_UP]:
                if not move_up_get_obstruct(player):
            	    dy = -1
            elif key[pg.K_DOWN]:
                if not move_down_get_obstruct(player):
            	    dy = 1
            if dy != 0:
            	player.last_dy = dy
            	player.key_presed = True
            	player.finished_y_move = False

    return dx, dy

def cannot_divide_by_16(num):
    return num % 16 != 0

def make_divisible_by_16(num):
	if num > 0:
		while num % 16 != 0:
			num += 1
	elif num < 0:
		while num % 16 != 0:
			num -= 1
	return num

def expect_finish_pos(player):
	expected_x, expected_y = player.finish_pos
	if player.last_dx < 0:
		checker = floor(player.pos[0])
	elif player.last_dx > 0:
		checker = ceil(player.pos[0])
	else:
		checker = 0

	if cannot_divide_by_16(checker):
		expected_x = make_divisible_by_16(checker)
	if checker == 0:
		expected_x = 0

	if player.last_dy < 0:
		checker = floor(player.pos[1])
	elif player.last_dy > 0:
		checker = ceil(player.pos[1])
	else:
		checker = 0

	if cannot_divide_by_16(checker):
		expected_y = make_divisible_by_16(checker)
	if checker == 0:
		expected_y = 0
	
	return (expected_x, expected_y)

def get_distance_between(current_pos, expected_pos):
	if current_pos[0] > expected_pos[0]:
		diff_x = current_pos[0] - expected_pos[0]
	elif current_pos[0] < expected_pos[0]:
		diff_x = expected_pos[0] - current_pos[0]
	else:
		diff_x = 0

	if current_pos[1] > expected_pos[1]:
		diff_y = current_pos[1] - expected_pos[1]
	elif current_pos[1] < expected_pos[1]:
		diff_y = expected_pos[1] - current_pos[1]
	else:
		diff_y = 0
		
	return diff_x, diff_y

def move(player, dx, dy, dt):
	player.pos[0] += dx * player.speed * dt
	player.pos[1] += dy * player.speed * dt
