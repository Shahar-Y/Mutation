# board-related constants
MAP_SIZE = 60                                  # how many tiles in either direction of grid
TILE_WIDTH = 10                                # pixel sizes for grid squares
TILE_HEIGHT = TILE_WIDTH
TILE_MARGIN = 1
WINDOW_SIZE = (TILE_WIDTH + TILE_MARGIN) * MAP_SIZE + TILE_MARGIN

# game parameters
FOOD_DROPPED = int(30)
GAME_SPEED = 50
DONE = False                                    # variable to keep track if window is open

DROPPING_PACE = 2

# cell parameters
INIT_HUNGER = 0
FOOD_WORTH = 12
EATING_SIZE = 3
COLOR_CHANGE = 4
# cell mutation features
MUTATION_POINTS = 15
MUTATION_CHANCE = 3

INIT_SIZE = 1
MAX_SIZE = 10
MIN_SIZE = 1
SIZE_VALUE = 1

INIT_FOOD_WORTH = 10
MAX_FOOD_WORTH = 15
MIN_FOOD_WORTH = 5
FOOD_WORTH_VALUE = 1

INIT_SIGHT = 10
MAX_SIGHT = 10
MIN_SIGHT = 1
SIGHT_VALUE = 1

INIT_FOOD_TO_REPRO = 3
MAX_FOOD_TO_REPRO = 4
MIN_FOOD_TO_REPRO = 1
FOOD_TO_REPRO_VALUE = -2

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
MAX_RGB = 255
