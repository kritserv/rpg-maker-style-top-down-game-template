import pygame as pg

def load_asset():
	town1_img_x1 = pg.image.load(f"asset/img/scene/town1.png").convert()
	town1_width, town1_height = town1_img_x1.get_size()
	town1_img_x2 = pg.transform.scale(town1_img_x1, (town1_width*2, town1_height*2)).convert()
	town1_img_x3 = pg.transform.scale(town1_img_x1, (town1_width*3, town1_height*3)).convert()
	return town1_img_x1, town1_img_x2, town1_img_x3