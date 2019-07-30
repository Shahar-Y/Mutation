# board-related constants
MAP_SIZE = 30                                  # how many tiles in either direction of grid
TILE_WIDTH = 18                                # pixel sizes for grid squares
TILE_HEIGHT = TILE_WIDTH
TILE_MARGIN = 1
WINDOW_SIZE = (TILE_WIDTH + TILE_MARGIN) * MAP_SIZE + TILE_MARGIN

# game parameters
FOOD_DROPPED = int(2)
GAME_SPEED = 17
DONE = False                                    # variable to keep track if window is open

DROPPING_PACE = 2

# cell parameters
DEFAULT_SIGHT = 10
INIT_HUNGER = 0
INIT_SIZE = 1
FOOD_WORTH = 15
REPRO_HEALTH = 40
EATING_SIZE = 3
COLOR_CHANGE = 4

# color constants
BLACK = (0, 0, 0)                             # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRASS = (255, 255, 255)
RED = (255, 0, 0)
FOOD_COLOR = (50, 255, 50)
BLUE = (0, 0, 255)
BLUE3 = (0, 50, 250)
BLUE2 = (0, 150, 250)
BLUE1 = (0, 220, 250)
