WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

CELL_SIZE = 30  # Size of each cell in pixels
GRID_SIZE = 16

# Calculate total grid size in pixels
GRID_WIDTH = CELL_SIZE * GRID_SIZE
GRID_HEIGHT = CELL_SIZE * GRID_SIZE

# Offset to center the grid
OFFSET_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
OFFSET_Y = ((WINDOW_HEIGHT+100) - GRID_HEIGHT) // 2

# Line thicknesses
THIN_LINE = 1    # Normal grid lines
MEDIUM_LINE = 2  # Every 5 cells
THICK_LINE = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (105, 105, 105)
SILVER = (211, 211, 211)
YELLOW = (255, 223, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CLEAR = (255, 255, 255, 0)