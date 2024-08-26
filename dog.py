#!/usr/bin/env python
import pygame as pg
import spritesheet
import spritesfunctions as sf
from enum import Enum
import random

# region enums

class Directions():
	def __init__(self):
		self.LEFT = 0
		self.LEFT_NAME = "left"
		self.RIGHT = 1
		self.RIGHT_NAME = "right"

class Actions():
	def __init__(self):
		self.LICK = 0
		self.LICK_NAME = "lick"
		self.WALK = 1
		self.WALK_NAME = "walk"
		self.RUN = 2
		self.RUN_NAME = "run"
		self.SIT = 3
		self.SIT_NAME = "sit"
		self.SIT_IDLE = 4
		self.SIT_IDLE_NAME = "sit idle"
		self.STAND_IDLE = 5
		self.STAND_IDLE_NAME = "stand idle"
		self.STAND = 6
		self.STAND_NAME = "stand"
# endregion

class Dog():

# region constructors
	def __init__(self, direction, action, screen_dest):
		# member variables
		self.direction = direction
		self.action = action
		self.frame = 0
		self.animation_cooldown = 100  # milliseconds
		self.last_update = pg.time.get_ticks()
		self.screen_dest = screen_dest  # @todo: make functions for screen_dest mutation
		# constants
		self.SPRITE_WIDTH = 60
		self.SPRITE_HEIGHT = 38
		self.BLACK = (0, 0, 0)
		self.Dirs = Directions()
		self.Acts = Actions()
		# number of frames in each animation
		self.ANIMATION_STEPS = [4, 6, 5, 3, 4, 4]
		self.NUM_ANIMATIONS = 7  # lick, walk, run, sit, sit idle, stand idle, stand

		self.sprite_sheet_image_left = pg.image.load(
			'./Sprites/Dog_medium_Left.png').convert_alpha()
		self.sprite_sheet_left = spritesheet.SpriteSheet(
			self.sprite_sheet_image_left)

		self.sprite_sheet_image_right = pg.image.load(
			'./Sprites/Dog_medium_Right.png').convert_alpha()
		self.sprite_sheet_right = spritesheet.SpriteSheet(
			self.sprite_sheet_image_right)

		self.animation_list = []
		sf.createAnimationListLeft(self.animation_list, self.ANIMATION_STEPS,
								   self.sprite_sheet_left, self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.BLACK)
		sf.createAnimationListRight(self.animation_list, self.ANIMATION_STEPS,
									self.sprite_sheet_right, self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.BLACK)

		# seed random
		random.seed()
# endregion

# region accessors
	def get_direction(self):
		return self.direction

	def get_action(self):
		if self.direction == self.Dirs.LEFT:
			return self.action
		else:
			return self.action - self.NUM_ANIMATIONS

	def get_frame(self):
		return self.frame

	def get_animation_cooldown(self):
		return self.animation_cooldown

	def get_last_update(self):
		return self.last_update

	def get_screen_dest(self):
		return self.screen_dest
# endregion

# region mutators
	def set_direction(self, direction):
		if direction == self.Dirs.LEFT or direction == self.Dirs.RIGHT:
			self.direction = direction
		else:
			raise Exception("invalid value for direction: ", direction)

	def set_action(self, action):
		if action >= 0 and action < self.NUM_ANIMATIONS * 2:
			self.action = action
			self.frame = 0
		else:
			raise Exception("invalid value for action: ", action)
# endregion

# region class utility functions
	def __change_action(self, new_action):
		if self.direction == self.Dirs.LEFT:
			self.action = new_action
			self.frame = 0
		else:
			self.action = new_action + self.NUM_ANIMATIONS
			self.frame = 0

	def change_action_random(self):
		self.__change_action(random.randint(0, self.NUM_ANIMATIONS - 1))

	def change_action_random_exclude_transitions_sit_idle(self):
		new_action = -1
		while new_action == -1 or new_action == self.Acts.SIT or new_action == self.Acts.STAND or new_action == self.Acts.SIT_IDLE:
			new_action = random.randint(0, self.NUM_ANIMATIONS - 1)
		self.__change_action(new_action)

# endregion

# region helper functions
	def update_animation(self, screen):
		current_time = pg.time.get_ticks()
		if current_time - self.last_update >= self.animation_cooldown:
			self.frame += 1
			self.last_update = current_time
			if self.frame >= len(self.animation_list[self.action]):
				self.frame = 0
		# show frame image
		screen.blit(self.animation_list[self.action]
					[self.frame], self.screen_dest)
# endregion

# region change directions
	def turn_left(self):
		self.direction = self.Dirs.LEFT
		if self.action >= self.NUM_ANIMATIONS:
			self.action -= self.NUM_ANIMATIONS

	def turn_right(self):
		self.direction = self.Dirs.RIGHT
		if self.action < self.NUM_ANIMATIONS:
			self.action += self.NUM_ANIMATIONS
# endregion

# region change actions
	def lick(self):
		if self.action != self.Acts.LICK and self.action != self.Acts.LICK + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.LICK)

	def walk(self):
		if self.action != self.Acts.WALK and self.action != self.Acts.WALK + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.WALK)

	def run(self):
		if self.action != self.Acts.RUN and self.action != self.Acts.RUN + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.RUN)

	def sit(self):
		if self.action != self.Acts.SIT and self.action != self.Acts.SIT + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.SIT)
			# transtion from sit to sit idle
			# @todo: transition currently doesn't take into account animation cooldown

	def sit_idle(self):
		if self.action != self.Acts.SIT_IDLE and self.action != self.Acts.SIT_IDLE + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.SIT_IDLE)

	def stand(self):
		if self.action != self.Acts.STAND and self.action != self.Acts.STAND + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.STAND)
			# transtion from stand to stand idle
			# @todo: transition currently doesn't take into account animation cooldown

	def stand_idle(self):
		if self.action != self.Acts.STAND_IDLE and self.action != self.Acts.STAND_IDLE + self.NUM_ANIMATIONS:
			self.__change_action(self.Acts.STAND_IDLE)
# endregion

# region determine specific direction states
	def is_facing_left(self):
		return self.direction == self.Dirs.LEFT

	def is_facing_right(self):
		return self.direction == self.Dirs.RIGHT
# endregion

# region determine specific action states
	def is_sitting(self):
		return self.action == self.Acts.SIT_IDLE or self.action == self.Acts.SIT_IDLE + self.NUM_ANIMATIONS

	def is_standing(self):
		return self.action == self.Acts.STAND_IDLE or self.action == self.Acts.STAND_IDLE + self.NUM_ANIMATIONS

	def is_walking(self):
		return self.action == self.Acts.WALK or self.action == self.Acts.WALK + self.NUM_ANIMATIONS

	def is_running(self):
		return self.action == self.Acts.RUN or self.action == self.Acts.RUN + self.NUM_ANIMATIONS

	def is_licking(self):
		return self.action == self.Acts.LICK or self.action == self.Acts.LICK + self.NUM_ANIMATIONS
# endregion
