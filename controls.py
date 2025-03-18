import pygame

from Sattings import *


pencil = pygame.image.load("image/pencil.png")
pencil_rect = pencil.get_rect()
pencil_rect.center = (65, 35)

DOT_BUTTON = pygame.Rect(10, 20, 30, 30)
LINE_BUTTON = pygame.Rect(10, 60, 30, 30)
PENCIL_BUTTON = pygame.Rect(50, 20, 30, 30)
CIRCLE_BUTTON = pygame.Rect(50, 60, 30, 30)
BUTTONS_ART = (DOT_BUTTON, LINE_BUTTON, PENCIL_BUTTON, CIRCLE_BUTTON)


RED_COLOR = [BRIGHT_RED, pygame.Rect(210, 20, 30, 30)]
BLUE_COLOR = [BRIGHT_BLUE, pygame.Rect(210, 60, 30, 30)]
YELLOW_COLOR = [BRIGHT_YELLOW, pygame.Rect(250, 20, 30, 30)]
GREEN_COLOR = [BRIGHT_GREEN, pygame.Rect(250, 60, 30, 30)]
BLACK_COLOR = [BLACK, pygame.Rect(290, 20, 30, 30)]
WHITE_COLOR = [WHITE, pygame.Rect(290, 60, 30, 30)]
CLEAR_COLOR = [CLEAR, pygame.Rect(330, 20, 30, 30)]
COSTUME_COLOR = [DARK_GRAY_RED, pygame.Rect(330, 60, 30, 30)]

BUTTONS_COLOR = []
r_b = 0
c_b = 0
for color in color_names:
    x = 210 + 22 * c_b
    y = 20 + 22 * r_b
    BUTTONS_COLOR.append([color, pygame.Rect(x, y, 20, 20)])
    if r_b == 2:
        c_b += 1
        r_b = 0
    else:
        r_b += 1

class Controls:
    def __init__(self, rectangle, looks):
        pass