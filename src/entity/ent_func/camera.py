def follow_or_stop_follow(cam, player):
	if cam.stop_follow_player_left_at_pos_x:
		if player.pos[0] < cam.stop_follow_player_left_at_pos_x:
			cam.follow_player_x_left = False
		else:
			cam.follow_player_x_left = True

	if cam.stop_follow_player_right_at_pos_x:
			if player.pos[0] > cam.stop_follow_player_right_at_pos_x:
				cam.follow_player_x_right = False
			else:
				cam.follow_player_x_right = True

	if cam.stop_follow_player_up_at_pos_y:
		if player.pos[1] < cam.stop_follow_player_up_at_pos_y:
			cam.follow_player_y_up = False
		else:
			cam.follow_player_y_up = True

	if cam.stop_follow_player_down_at_pos_y:
			if player.pos[1] > cam.stop_follow_player_down_at_pos_y:
				cam.follow_player_y_down = False
			else:
				cam.follow_player_y_down = True