#We import os to build file paths
import os

#Screen resolution of the game window (width and height)
SCREEN_W, SCREEN_H = 1920, 1080
#Frames per second target, how fast we will update and draw the game. 
FPS = 60

#Assets of the game (images, fonts and saved scores)
#folder where I stored every visual elements for the game
ASSETS_DIR = "assets"
BACKGROUND_FILE = "background.png" #main background for the gameplay
MENU_BG_FILE = "menu_background.png" #image for the first page of the game (menu)
SCOREBOARD_BG_FILE = "scoreboard_background.png" #image for the scoreboard
#The character sprites (3 images, still/idle, running right, running left)
CHAR_STILL_FILE = "character still.png"
CHAR_RUN_RIGHT_FILE = "character running right.png"
CHAR_RUN_LEFT_FILE = "character running left.png"
#Custom arcade font
ARCADE_FONT_FILE = "ByteBounce.ttf"
#Where the scoreboard is saved into a json file
SCORES_FILE = os.path.join(ASSETS_DIR, "scores.json")

#Player physics and visuals
#Size of the hitbox of the characcter (collision rectangle)
PLAYER_W, PLAYER_H = 32, 48
#Target height of the character by scaling the PNGs to this height
SPRITE_TARGET_H = 100
#Small offset so that the character's feet can line up nicely with the collision rectangle
FEET_OFFSET_Y = 10

#Default platform size when you start building platforms isn editor mode (E)
DEFAULT_PLAT_W = 160
DEFAULT_PLAT_H = 16
#Size of the goal collision area. Even though the goal is drawn visually as a glowing circle,
#the collision detection is handle using pygame.rect
GOAL_W, GOAL_H = 40, 60
#Platform colors (simple brown style)
PLATFORM_FILL = (140, 90, 45)
PLATFORM_OUTLINE = (0, 0, 0)
#Radius used to draw the glowing goal ring (for visual effect)
GOAL_RING_R = 14
#Window title is displayed at the top of the pygame window
WINDOW_TITLE = "TOWER OF IE: THE WIZARD CLIMB"

#Game states here in order to help us switch screens
#Going from menu -> name_input -> game -> scoreboard 
STATE_MENU = "menu"
STATE_NAME = "name"
STATE_SCOREBOARD = "scoreboard"
STATE_GAME = "game"