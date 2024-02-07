#!/usr/bin/env python

import mysql.connector as conn
import pygame as pg
from pygame import mixer
import random
import button
import dog
import sqlconn

# region debug/test values

# @todo: get rid of debug/test values
TEST_USER_ID = 1
# endregion

# mixer allows us to load sounds
# I have no idea what these mean, Coding with Russ on Youtube set these arguments like this
pg.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pg.init()

# region setup

# region screen setup
SCREEN_WIDTH = 928
SCREEN_HEIGHT = 793
BACKGROUND = pg.image.load('./Backgrounds/Free Pixel Art Forest/Preview/Background.png')

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Sit, Boy!')
random.seed()
# endregion

# region font setup
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
yellow = (255, 255, 0)

font_size = 32

sans_bold_font = pg.font.Font('fonts/Pixeloid/TrueType (.ttf)/PixeloidSans-Bold.ttf', font_size)

conclusion_text = sans_bold_font.render('The experiment has concluded.', True, white, black)
conclusion_text_rect = conclusion_text.get_rect()
conclusion_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

thankyou_text = sans_bold_font.render('Thank you for participating!', True, white, black)
thankyou_text_rect = thankyou_text.get_rect()
thankyou_text_rect.center = (
	SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + font_size*1.25)
# endregion

# region SQL setup
sqlEventHandler = sqlconn.SqlConn("", "", "", "")
# endregion
# endregion

game_running = True
menu_running = True

# region main methods
def input_is_correct(key, is_sitting):
	return is_sitting and (key == pg.K_KP_ENTER or key == pg.K_RETURN or key == pg.MOUSEBUTTONDOWN)

def shuffle_animations(anilist):
	while not list_is_good(anilist):
		random.shuffle(anilist)
	return anilist

def list_is_good(anilist):
	for i in range(len(anilist) - 2):
		if anilist[i][0] == dog.Actions.SIT_IDLE.value and anilist[i+1][0] == dog.Actions.SIT_IDLE.value:
			return False
	return True
	
# endregion

# region game menu

# load button images
start_img = pg.image.load('./Menu Buttons/Large Buttons/Large Buttons/Play Button.png').convert_alpha()
stop_img = pg.image.load('./Menu Buttons/Large Buttons/Large Buttons/Quit Button.png').convert_alpha()

# create button instances
start_button = button.Button(200, 100, start_img, .8)
quit_button = button.Button(200, 400, stop_img, .8)

# load menu music
pg.mixer.music.load('Music/Abstraction - Ludum Dare 28 Loops/Ludum Dare 28 - Track 1.wav')
pg.mixer.music.set_volume(.5)  # 50% original volume
pg.mixer.music.play(-1, 0.0, 5000)

# load menu sounds
confirm_fx = pg.mixer.Sound('sfx/menu/confirm tones/confirm_style_2_001.wav')
back_fx = pg.mixer.Sound('sfx/menu/back tones/back_style_2_001.wav')
error_fx = pg.mixer.Sound('sfx/menu/error tones/error_style_2_001.wav')
cursor_fx = pg.mixer.Sound('sfx/menu/cursor_style_2.wav')

# menu loop
while menu_running:
	screen.fill((202, 228, 241))

	# @todo: cursor_fx currently plays 6 seconds repeating as long as colliding with button. Cut the sfx down and make it only play once per mouseover.
	# if start_button.rect.collidepoint(pg.mouse.get_pos()) or quit_button.rect.collidepoint(pg.mouse.get_pos()):
	# 	cursor_fx.play()
	if start_button.draw(screen):
		confirm_fx.play()
		menu_running = False
	if quit_button.draw(screen):
		back_fx.play()
		menu_running = False
		game_running = False

	# event handler
	for event in pg.event.get():
		# quit game
		if event.type == pg.QUIT:
			menu_running = False
			game_running = False

	pg.display.update()
# endregion

session_happening = game_running
if game_running:
	sqlEventHandler.new_player_login(TEST_USER_ID)

# region sound management

# load game music
pg.mixer.music.load(
	'Music/Abstraction - Ludum Dare 28 Loops/Ludum Dare 28 - Track 8.wav')
pg.mixer.music.set_volume(.5)  # 50% original volume
pg.mixer.music.play(-1, 0.0, 5000)

# load game sounds
reward_fx = pg.mixer.Sound('sfx/game/MI_SFX 43.wav')

goodboi_dest = (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 160)
goodboi = dog.Dog(dog.Directions.LEFT.value,
				  dog.Actions.STAND_IDLE.value, goodboi_dest)
# endregion

# region setup animation distributions

# @todo: shuffle the animations to add randomization between plays
# level 1: sit idle and stand idle
level_1 = [(dog.Actions.STAND_IDLE.value, 2.5),
		   (dog.Actions.STAND_IDLE.value, 2),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.STAND_IDLE.value, 2),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.STAND_IDLE.value, 1),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.SIT_IDLE.value, 1),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 1.5),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 1),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 4),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 3)]  # sit_idle
level_1 = shuffle_animations(level_1)
print(level_1)

# level 2: sit idle, stand idle, walk
level_2 = [(dog.Actions.STAND_IDLE.value, 2.5),
		   (dog.Actions.STAND_IDLE.value, 2),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.WALK.value, 2),
		   (dog.Actions.WALK.value, 3),
		   (dog.Actions.WALK.value, 1),
		   (dog.Actions.WALK.value, 3),
		   (dog.Actions.SIT_IDLE.value, 1),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 1.5),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 1),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 4),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 3)]  # sit_idle
level_2 = shuffle_animations(level_2)

# level 3: sit idle, stand idle, walk, lick
level_3 = [(dog.Actions.STAND_IDLE.value, 2.5),
		   (dog.Actions.STAND_IDLE.value, 2),
		   (dog.Actions.STAND_IDLE.value, 3),
		   (dog.Actions.LICK.value, 3),
		   (dog.Actions.LICK.value, 1),
		   (dog.Actions.LICK.value, 2),
		   (dog.Actions.WALK.value, 3),
		   (dog.Actions.WALK.value, 1),
		   (dog.Actions.WALK.value, 3),
		   (dog.Actions.SIT_IDLE.value, 1.5),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 1),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 4),  # sit_idle
		   (dog.Actions.SIT_IDLE.value, 3)]  # sit_idle
level_3 = shuffle_animations(level_3)

list_index = 0
last_update = pg.time.get_ticks()
action_change_time = 1000 * level_1[0][1]  # milliseconds
# endregion

# region game loop
while game_running:
	# update background
	screen.blit(BACKGROUND, (0, 0))

	current_time = pg.time.get_ticks()
	if current_time - last_update >= action_change_time and list_index < len(level_1):
		goodboi.set_action(level_1[list_index][0])
		last_update = current_time
		sqlEventHandler.animation_change(TEST_USER_ID, goodboi.get_action())
		action_change_time = 1000 * level_1[list_index][1]  # milliseconds
		list_index += 1

	# update animation
	goodboi.update_animation(screen)

	if list_index >= len(level_1):
		screen.blit(conclusion_text, conclusion_text_rect)
		screen.blit(thankyou_text, thankyou_text_rect)

	# event handler
	for event in pg.event.get():

		if event.type == pg.QUIT:
			game_running = False
		if event.type == pg.KEYDOWN:
			sqlEventHandler.user_input(TEST_USER_ID, pg.key.name(event.key), goodboi.get_action(), input_is_correct(event.key, goodboi.is_sitting()))
			# user action handlers
			if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN or event.key == pg.MOUSEBUTTONDOWN:
				if goodboi.is_sitting():
					reward_fx.play()
					# @todo: give user feedback on-screen
				else:
					error_fx.play()
					# @todo: give user feedback on-screen
			# quit game
			elif event.key == pg.K_ESCAPE:
				game_running = False

			# @todo: delet this
			# hit backslash to test experiment-end code
			elif event.key == pg.K_BACKSLASH:
				list_index = len(level_1)

	pg.display.update()
# endregion
if session_happening:
	sqlEventHandler.session_end(TEST_USER_ID)
pg.quit()
