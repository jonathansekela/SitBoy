#!/usr/bin/env python
def createAnimationListLeft(animation_list, animation_steps, sprite_sheet, sprite_width, sprite_height, color):
	#lick, walk, run, sit, sit idle, stand idle, stand
	step_counter_x = 0
	step_counter_y = 0

	for animation in animation_steps:
		temp_img_list = []
		for i in range(animation):
			temp_img_list.append(sprite_sheet.get_image(i, step_counter_y, sprite_width, sprite_height, 3, color))
		
		animation_list.append(temp_img_list)
		step_counter_y += 1
		step_counter_x = 0

	#get reverse sit animation for stand animation
	temp_img_list = []
	for i in range(2, -1, -1):
		temp_img_list.append(sprite_sheet.get_image(i, 3, sprite_width, sprite_height, 3, color))
	animation_list.append(temp_img_list)

def createAnimationListRight(animation_list, animation_steps, sprite_sheet, sprite_width, sprite_height, color):
	#lick, walk, run, sit, sit idle, stand idle, stand
	step_counter_x = 0
	step_counter_y = 0

	for animation in animation_steps:
		temp_img_list = []
		for i in reversed(range(animation)):
			temp_img_list.append(sprite_sheet.get_image(i + (6 - animation), step_counter_y, sprite_width, sprite_height, 3, color))
		
		animation_list.append(temp_img_list)
		step_counter_y += 1
		step_counter_x = 0

	#get reverse sit animation for stand animation
	temp_img_list = []
	for i in range(3):
		temp_img_list.append(sprite_sheet.get_image(i + (6 - 3), 3, sprite_width, sprite_height, 3, color))
	animation_list.append(temp_img_list)