import pygame
import pygame_gui
# import tkinter as tk
# from tkinter import filedialog
from Sattings import *
from controls import *
from Cell import *
from PIL import Image

# Initialize Pygame0
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixle Paint")

init_color = BLACK
save_message = ""
save_message_timer = 0
savebutton = 1
save_button = (1, 2, 50, 15)
# workspace maker

work_page = Image.new('RGBA', (GRID_SIZE, GRID_SIZE), (0, 0, 0, 0))

# UI
MANAGER = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
red_mix = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((400, 10), (80, 20)),
    manager=MANAGER,
    object_id="#red_mix",
    placeholder_text="0 - 255"
)
blue_mix = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((400, 40), (80, 20)),
    manager=MANAGER,
    object_id="#blue_mix",
    placeholder_text="0 - 255"
)
green_mix = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((400, 70), (80, 20)),
    manager=MANAGER,
    object_id="#green_mix",
    placeholder_text="0 - 255"
)


def privet_color():
    try:
        r = int(red_mix.get_text())
        b = int(blue_mix.get_text())
        g = int(green_mix.get_text())
        COSTUME_COLOR[0] = (r, b, g)
    except:
        COSTUME_COLOR[0] = RED


def save_artwork(filename="my_art.png"):
    # Access the global work_page and grid
    global work_page, grid

    # Update the work_page with the current colors from the grid
    pixels = work_page.load()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_color = grid[y][x].color  # Get the cell's current color
            if len(cell_color) == 3:
                cell_color = cell_color + (255,)
            pixels[x, y] = cell_color

    # Save the image to a file
    try:
        work_page.save(filename)
        return f"Saved successfully as {Free.png}"
    except Exception as e:
        return f"Error saving file: {str(e)}"


# Font for text
font = pygame.font.Font(None, 36)
manu_font = pygame.font.Font(None, 20)

# Button properties
button_rect = pygame.Rect(300, 250, 200, 50)
button_text = font.render("Open File", True, BLACK)

# Variable to store the selected file
selected_file = "No file selected"

# Set up the square properties
reck_width = WINDOW_WIDTH
reck_hight = 100
square_x = 0
square_y = 0

selected_button_index = 0

grid = []
pixels = work_page.load()
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        # Calculate the position of the cell on the screen
        pixel_x = OFFSET_X + x * CELL_SIZE
        pixel_y = OFFSET_Y + y * CELL_SIZE
        # Create a Cell object with row, col, x, y, size, and initial color
        initial_color = pixels[x, y][:3]  # Convert RGBA to RGB for Pygame
        cell = Cell(y, x, pixel_x, pixel_y, CELL_SIZE, CLEAR)
        row.append(cell)
    grid.append(row)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    # Check for events
    for event in pygame.event.get():
        MANAGER.process_events(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(save_button).collidepoint(event.pos):
                save_message = save_artwork()
                save_message_timer = 120
        if save_message and save_message_timer > 0:
            save_message_surface = font.render(save_message, True, BLACK)
            save_message_rect = save_message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            screen.blit(save_message_surface, save_message_rect)
            save_message_timer -= 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, button in enumerate(BUTTONS_ART):
                if button.collidepoint(event.pos):
                    selected_button_index = index
                    break
        if event.type == pygame.MOUSEBUTTONDOWN:
            for COLOR, button in BUTTONS_COLOR:
                if button.collidepoint(event.pos):
                    init_color = COLOR
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in grid:
                for cell in row:
                    if cell.rect.collidepoint(event.pos):
                        cell.paint(init_color)
                        print(red_mix.get_text())

    # Clear the screen
    screen.fill(SILVER)

    for row in grid:
        for cell in row:
            cell.draw(screen)

    # Draw grid lines
    for x in range(GRID_SIZE + 1):
        pixel_x = OFFSET_X + x * CELL_SIZE
        if x % 16 == 0:  # Thickest line every 20 cells
            thickness = THICK_LINE
            color = BLACK
        elif x % 4 == 0:  # Medium line every 5 cells
            thickness = MEDIUM_LINE
            color = BLACK
        else:  # Normal thin line
            thickness = THIN_LINE
            color = GRAY
        pygame.draw.line(screen, color, (pixel_x, OFFSET_Y), (pixel_x, OFFSET_Y + GRID_HEIGHT), thickness)
    for y in range(GRID_SIZE + 1):
        pixel_y = OFFSET_Y + y * CELL_SIZE
        if y % 16 == 0:  # Thickest line every 20 cells
            thickness = THICK_LINE
            color = BLACK
        elif y % 4 == 0:  # Medium line every 5 cells
            thickness = MEDIUM_LINE
            color = BLACK
        else:  # Normal thin line
            thickness = THIN_LINE
            color = GRAY
        pygame.draw.line(screen, color, (OFFSET_X, pixel_y), (OFFSET_X + GRID_WIDTH, pixel_y), thickness)

    # Draw the square
    pygame.draw.rect(screen, GRAY, (square_x, square_y, reck_width, reck_hight))
    for index, button in enumerate(BUTTONS_ART):
        if index == selected_button_index:  # Highlight the selected button
            pygame.draw.rect(screen, YELLOW, button)
        else:
            pygame.draw.rect(screen, SILVER, button)
    for BUTTON_COLOR in BUTTONS_COLOR:
        pygame.draw.rect(screen, BUTTON_COLOR[0], BUTTON_COLOR[1])

    MANAGER.update(time_delta)
    MANAGER.draw_ui(screen)
    screen.blit(font.render("R", True, RED), (370, 10))
    screen.blit(font.render("B", True, BLUE), (370, 40))
    screen.blit(font.render("G", True, GREEN), (370, 70))
    pygame.draw.line(screen, BLACK, (200, 0), (200, 95), 2)

    pygame.draw.line(screen, BLACK, (11, 88), (37, 62), 3)
    pygame.draw.circle(screen, BLACK, (25, 35), 5)
    privet_color()

    # save load

    pygame.draw.rect(screen, BLACK, save_button)
    screen.blit(manu_font.render("Save", True, WHITE), save_button)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
