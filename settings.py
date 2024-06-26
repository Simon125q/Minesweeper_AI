import pygame
from enum import Enum

pygame.init()


FPS = 60
GRID_SIZE = 25
TILE = 20
MENU_WIDTH = 260
WIDTH, HEIGHT = RES = (GRID_SIZE * TILE + MENU_WIDTH, GRID_SIZE * TILE)

FONT_SIZE = TILE
FONT = pygame.font.Font(None, FONT_SIZE)

class State(Enum):
    UNVISITED = '#dedcd7'
    VISITED = '#999999'
    FLAG = 'red'
    BOMB = 'black'
    
BOMB_NUM = int(GRID_SIZE * GRID_SIZE * 0.15)
    
# Menu
BUTTON_SPACING = 35
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 170
MENU_FONT = pygame.font.Font(None, 30)
MENU_FONT_SIZE = 30
MENU_FONT_COLOR = '#e0e1dd'
BUTTON_COLOR_SELECTED = '#415a77'
BUTTON_COLOR = '#778da9'
BUTTON_COLOR_BORDER = '#1b263b'
MATCHING_RED = '#BC4749'
AI_MOVE = 0
AI_SOLVE = 1
RESET = 2
EXIT = 3