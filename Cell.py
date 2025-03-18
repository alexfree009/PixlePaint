import pygame
from Sattings import *

class Cell:
    def __init__(self, row, col, x, y, size, color=WHITE):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(x, y, size, size)  # Rectangle for drawing and collision
        self.color = color  # Use the provided color or default to WHITE
        self.is_clicked = False  # Track click state
        self.id = f"{row},{col}"  # Unique ID for each cell (e.g., "0,0")

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
                self.color = BRIGHT_RED  # Turn red when clicked
                print(f"Cell {self.id} clicked!")
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.is_clicked:
                self.is_clicked = False
                self.color = WHITE

    def paint(self, new_color):
        self.color = new_color
    def sqair_draw(self, new_color):
        pass