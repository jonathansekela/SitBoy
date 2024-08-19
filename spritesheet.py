#!/usr/bin/env python
import pyjsdl as pg

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame_x, frame_y, width, height, scale, color):
		image = pg.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), (frame_x * width, frame_y * height, width, height))
		image = pg.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(color)

		return image