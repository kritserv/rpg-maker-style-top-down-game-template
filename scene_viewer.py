from json import load
import matplotlib.pyplot as plt
import matplotlib.patches as patches

white = (255, 255, 255)
blue = (67, 110, 238)

def convert_char(char, val_dict):
	try:
		return val_dict[char]
	except KeyError:
		try:
			return int(char)
		except ValueError:
			return char

def build_multiple_pg_rect(method, x, y):
	rects = []
	with open("game_data/scene/method.json") as f:
		json_load = load(f)
		loaded_method = json_load["build_multiple_pg_rect"]
		f.close()
	build_calculation = loaded_method[method]
	for calculation in build_calculation:
		rect = []
		for value in calculation:
			if type(value) == str:
				has_operator = False
				for operator in ["+", "-"]:
					if operator in value:
						has_operator = True
						value_0, value_1 = [convert_char(char, {"x": x, "y": y}) for char in value.split(operator)]
						if operator == "+":
							cal_value = value_0 + value_1
						elif operator == "-":
							cal_value = value_0 - value_1
						rect.append(cal_value)
				if not has_operator:
					rect.append(convert_char(value, {"x": x, "y": y}))
			elif type(value) == int:
				rect.append(value)
		rect = [rect, blue]
		rects.append(rect)
	return rects

def load_scene_from_json():
	with open("game_data/scene/data.json") as f:
		json_load = load(f)
		loaded_scene_data = json_load["scene_data"]
		f.close()
	with open("game_data/scene/config.json") as f:
		json_load = load(f)
		loaded_scene_dict = json_load["scene_dict"]
		f.close()

	scene_data = {}

	if loaded_scene_data["get_pg_rect_by_method"]:
		for calculation in loaded_scene_data["get_pg_rect_by_method"]:
			for rect_group_name, value in calculation.items():
				method, x, y = value
				scene_data[rect_group_name] = build_multiple_pg_rect(method, x, y)

	if loaded_scene_data["pg_rect"]:
		for rect_group in loaded_scene_data["pg_rect"]:
			for rect_group_name, rect_group_list in rect_group.items():
				for rect in rect_group_list:
					try:
						scene_data[rect_group_name].append([rect, white])
					except KeyError:
						scene_data[rect_group_name] = [[rect, white]]

	scene_dict = {}

	if loaded_scene_dict:
		for scene_group_name, scene_group_list in loaded_scene_dict.items():
			total_scene_group = []
			for scene_group in scene_group_list:
				total_scene_group += scene_data[scene_group]

			scene_dict[scene_group_name] = total_scene_group

	return scene_dict


def render_map(map_name):

	fig, ax = plt.subplots()

	ax.set_title(map_name)
	ax.set_facecolor("black")
	rects = scene_dict[map_name]
	for rect in rects:
		xy = (rect[0][0], -rect[0][1])
		width = rect[0][2]
		height = -rect[0][3]
		color = tuple([x/255 for x in rect[1]])
		ax.add_patch(patches.Rectangle(xy, width, height, facecolor=color))
	ax.set_aspect("equal", "box")
	ax.relim()
	ax.autoscale_view()
	ax.set_xlim([-320, 320])
	ax.set_ylim([-320, 320])
	plt.show()

def render_all_map():
	for map_name in scene_dict:
		render_map(map_name)

scene_dict = load_scene_from_json()

if __name__ == "__main__":
	print("\nAvailable maps:")
	for map_name in scene_dict:
		print(map_name)

	while True:
		user_input = input("\nEnter a map name to render (or 'all' to render all maps, 'q' to quit)\n: ")

		if user_input == "q" or user_input == "quit":
			break

		elif user_input == "all":
			render_all_map()

		elif user_input in scene_dict:
			render_map(user_input)

		else:
			print(f"Error: {user_input} is not a recognized command or map name.")
