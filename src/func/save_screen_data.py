from .save_json_file import save_to_json

def save_screen_setting(full_screen, black_bar, cap_fps, target_fps):
	settings = {
		"fullscreen": str(full_screen),
		"blackbar": str(black_bar),
		"capfps": str(cap_fps),
		"capfps_at": target_fps
	}
	save_to_json("user_data/settings.json", settings)