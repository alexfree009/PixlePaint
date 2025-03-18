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
pygame.display.set_caption("Pixel Paint")

mode_active = 1
color_set = BLACK
save_message = ""
save_message_timer = 0
savebutton = 1
initial_point = (0, 0)

save_button = (100, 2, 50, 15)
load_button = (152, 2, 50, 15)
# workspace maker

work_page = Image.new('RGBA', (GRID_SIZE, GRID_SIZE), (0, 0, 0, 0))

# UI
MANAGER = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
red_mix = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((550, 10), (40, 20)),
    manager=MANAGER,
    object_id="#red_mix",
    initial_text=str(color_set[0])
)
blue_mix = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((550, 40), (40, 20)),
    manager=MANAGER,
    object_id="#green_mix",
    initial_text=str(color_set[1])
)
green_mix = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((550, 70), (40, 20)),
    manager=MANAGER,
    object_id="#blue_mix",
    initial_text=str(color_set[2])
)
save_load = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((1, 0), (98, 20)),
    manager=MANAGER,
    object_id="#save_load",
    placeholder_text="file_name"
)
save_load_text = "no_name"
def save_lode_fix():
    global save_load_text
    save_load_text = "image/" + save_load.get_text() + ".png"


def privet_color():
    try:
        r = int(red_mix.get_text())
        b = int(blue_mix.get_text())
        g = int(green_mix.get_text())
        if r > 255:
            r = 255
        if b > 255:
            b = 255
        if g > 255:
            g = 255
        COSTUME_COLOR[0] = (r, b, g)
    except ValueError:
        COSTUME_COLOR[0] = DARK_GRAY_RED

def save_artwork(save_load_text):
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
        work_page.save(save_load_text)
        return f"Saved successfully as {save_load_text}"
    except Exception as e:
        return f"Error saving file: {str(e)}"


def load_artwork(save_load_text):
    global work_page, grid
    try:
        loaded_image = Image.open(save_load_text)
        if loaded_image.size != (GRID_SIZE, GRID_SIZE):
            return f"Error: Loaded image size {loaded_image.size} does not match grid size ({GRID_SIZE}, {GRID_SIZE})"
        if loaded_image.mode != 'RGBA':
            loaded_image = loaded_image.convert('RGBA')
        work_page = loaded_image
        pixels = work_page.load()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                grid[y][x].color = pixels[x, y]
        return f"Loaded successfully from {save_load_text}"
    except Exception as e:
        return f"Error loading file: {str(e)}"


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
        pixel_x = OFFSET_X + x * CELL_SIZE
        pixel_y = OFFSET_Y + y * CELL_SIZE
        initial_color = pixels[x, y][:3]
        cell = Cell(y, x, pixel_x, pixel_y, CELL_SIZE, CLEAR)
        row.append(cell)
    grid.append(row)

# Game loop
clock = pygame.time.Clock()
holding = False
running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    # events
    for event in pygame.event.get():
        MANAGER.process_events(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            holding = True
            mouse_pos = event.pos

            if pygame.Rect(save_button).collidepoint(event.pos):
                save_message = save_artwork(save_load_text)
                save_message_timer = 120

            if pygame.Rect(load_button).collidepoint(event.pos):
                load_message = load_artwork(save_load_text)
                save_message_timer = 120

            for index, button in enumerate(BUTTONS_ART):
                if button.collidepoint(event.pos):
                    selected_button_index = index
                    break

            for COLOR, button in BUTTONS_COLOR:
                if button.collidepoint(event.pos):
                    color_set = COLOR
                    break

            if mode_active == 0:
                for row in grid:
                    for cell in row:
                        if cell.rect.collidepoint(mouse_pos):
                            cell.paint(color_set)
        if event.type == pygame.MOUSEBUTTONUP:
            holding = False

        if holding and mode_active == 1:
            m = pygame.mouse.get_pos()
            for row in grid:
                for cell in row:
                    if cell.rect.collidepoint(m):
                        cell.paint(color_set)
        if holding and mode_active == 2:
            m = pygame.mouse.get_pos()
            for row in grid:
                for cell in row:
                    if cell.rect.collidepoint(m):
                        for x, y in mouse_pos:
                            for xm, ym in m:
                                if x > xm:
                                    pass

    screen.fill(DARK_GRAY)

    # Parchment maker
    for row in grid:
        for cell in row:
            cell.draw(screen)

    for x in range(GRID_SIZE + 1):
        pixel_x = OFFSET_X + x * CELL_SIZE
        if x % 16 == 0:
            thickness = THICK_LINE
            color = BLACK
        elif x % 4 == 0:
            thickness = MEDIUM_LINE
            color = BLACK
        else:
            thickness = THIN_LINE
            color = GRAY
        pygame.draw.line(screen, color, (pixel_x, OFFSET_Y), (pixel_x, OFFSET_Y + GRID_HEIGHT), thickness)

    for y in range(GRID_SIZE + 1):
        pixel_y = OFFSET_Y + y * CELL_SIZE
        if y % 16 == 0:
            thickness = THICK_LINE
            color = BLACK
        elif y % 4 == 0:
            thickness = MEDIUM_LINE
            color = BLACK
        else:
            thickness = THIN_LINE
            color = GRAY
        pygame.draw.line(screen, color, (OFFSET_X, pixel_y), (OFFSET_X + GRID_WIDTH, pixel_y), thickness)

    # Draw the square
    pygame.draw.rect(screen, GRAY, (square_x, square_y, reck_width, reck_hight))
    for index, button in enumerate(BUTTONS_ART):
        color = BRIGHT_YELLOW if index == selected_button_index else DARK_GRAY
        pygame.draw.rect(screen, color, button)

    for BUTTON_COLOR in BUTTONS_COLOR:
        pygame.draw.rect(screen, BUTTON_COLOR[0], BUTTON_COLOR[1])

    MANAGER.update(time_delta)
    MANAGER.draw_ui(screen)

    #screen.blit(font.render("R", True, RED), (370, 10))
    #screen.blit(font.render("B", True, BLUE), (370, 40))
    #screen.blit(font.render("G", True, GREEN), (370, 70))

    pygame.draw.line(screen, BLACK, (200, 0), (200, 95), 2)
    pygame.draw.line(screen, BLACK, (11, 88), (37, 62), 3)
    pygame.draw.circle(screen, BLACK, (25, 35), 5)
    screen.blit(pencil, pencil_rect)

    if save_message and save_message_timer > 0:
        save_message_surface = font.render(save_message, True, BLACK)
        save_message_rect = save_message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        screen.blit(save_message_surface, save_message_rect)
        save_message_timer -= 1

    # save load

    pygame.draw.rect(screen, BLACK, save_button)
    screen.blit(manu_font.render("Save", True, WHITE), save_button)

    pygame.draw.rect(screen, BLACK, load_button)
    screen.blit(manu_font.render("Load", True, WHITE), load_button)
    green_mix.set_text(str(color_set[2]))
    blue_mix.set_text(str(color_set[1]))
    red_mix.set_text(str(color_set[0]))

    save_lode_fix()
    privet_color()
    pygame.display.flip()

# Quit Pygame
pygame.quit()
