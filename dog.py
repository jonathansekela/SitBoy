#!/usr/bin/env python
import pygame as pg
import spritesheet
import spritesfunctions as sf
from enum import Enum
import random

# region enums

class Directions(Enum):
	LEFT = 0
	RIGHT = 1

class Actions(Enum):
	LICK = 0
	WALK = 1
	RUN = 2
	SIT = 3
	SIT_IDLE = 4
	STAND_IDLE = 5
	STAND = 6
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
		if self.direction == Directions.LEFT.value:
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
		if direction == Directions.LEFT.value or direction == Directions.RIGHT.value:
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
		if self.direction == Directions.LEFT.value:
			self.action = new_action
			self.frame = 0
		else:
			self.action = new_action + self.NUM_ANIMATIONS
			self.frame = 0

	def change_action_random(self):
		self.__change_action(random.randint(0, self.NUM_ANIMATIONS - 1))

	def change_action_random_exclude_transitions_sit_idle(self):
		new_action = -1
		while new_action == -1 or new_action == Actions.SIT.value or new_action == Actions.STAND.value or new_action == Actions.SIT_IDLE.value:
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
		self.direction = Directions.LEFT.value
		if self.action >= self.NUM_ANIMATIONS:
			self.action -= self.NUM_ANIMATIONS

	def turn_right(self):
		self.direction = Directions.RIGHT.value
		if self.action < self.NUM_ANIMATIONS:
			self.action += self.NUM_ANIMATIONS
# endregion

# region change actions
	def lick(self):
		if self.action != Actions.LICK.value and self.action != Actions.LICK.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.LICK.value)

	def walk(self):
		if self.action != Actions.WALK.value and self.action != Actions.WALK.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.WALK.value)

	def run(self):
		if self.action != Actions.RUN.value and self.action != Actions.RUN.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.RUN.value)

	def sit(self):
		if self.action != Actions.SIT.value and self.action != Actions.SIT.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.SIT.value)
			# transtion from sit to sit idle
			# @todo: transition currently doesn't take into account animation cooldown

	def sit_idle(self):
		if self.action != Actions.SIT_IDLE.value and self.action != Actions.SIT_IDLE.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.SIT_IDLE.value)

	def stand(self):
		if self.action != Actions.STAND.value and self.action != Actions.STAND.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.STAND.value)
			# transtion from stand to stand idle
			# @todo: transition currently doesn't take into account animation cooldown

	def stand_idle(self):
		if self.action != Actions.STAND_IDLE and self.action != Actions.STAND_IDLE.value + self.NUM_ANIMATIONS:
			self.__change_action(Actions.STAND_IDLE.value)
# endregion

# region determine specific direction states
	def is_facing_left(self):
		return self.direction == Directions.LEFT.value

	def is_facing_right(self):
		return self.direction == Directions.RIGHT.value
# endregion

# region determine specific action states
	def is_sitting(self):
		return self.action == Actions.SIT_IDLE.value or self.action == Actions.SIT_IDLE.value + self.NUM_ANIMATIONS

	def is_standing(self):
		return self.action == Actions.STAND_IDLE.value or self.action == Actions.STAND_IDLE.value + self.NUM_ANIMATIONS

	def is_walking(self):
		return self.action == Actions.WALK.value or self.action == Actions.WALK.value + self.NUM_ANIMATIONS

	def is_running(self):
		return self.action == Actions.RUN.value or self.action == Actions.RUN.value + self.NUM_ANIMATIONS

	def is_licking(self):
		return self.action == Actions.LICK.value or self.action == Actions.LICK.value + self.NUM_ANIMATIONS
# endregion
