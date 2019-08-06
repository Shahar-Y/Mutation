import time
import math
from typing import List
import pygame
from enums import TileType
from board import Cell, BOARD
import constants as C

pygame.init()                                 # start up dat pygame
# for frame-rate or something? still not very sure
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(
    [C.WINDOW_SIZE, C.WINDOW_SIZE])  # making the window

def size_to_percentage(num):
    return math.sqrt(num)/math.sqrt(C.MAX_SIZE)

def int_to_direction(num):
    if num % 4 == 0:
        return "LEFT"
    if num % 4 == 1:
        return "RIGHT"
    if num % 4 == 2:
        return "UP"
    if num % 4 == 3:
        return "DOWN"
    return "LEFT"

def run_game():
    done = False
    loop_counter = 0
    food_dropped = C.FOOD_DROPPED
    game_speed = C.INIT_GAME_SPEED
    while not done:     # Main pygame loop
        loop_counter += 1
        time.sleep(0.01*(C.MAX_GAME_SPEED-game_speed))

        print(str(BOARD.num_cells))

        # get all cells on board
        cells = []
        for col in range(C.MAP_SIZE):
            for row in range(C.MAP_SIZE):
                if BOARD.Grid[col][row].type == TileType.Cell:
                    cells.append(BOARD.Grid[col][row])
        cells.sort(key=lambda cell: cell.size, reverse=True)

        # all cells make a step and those who starved are added to the dead pool
        dead_pool: List[Cell] = []
        for _, cell in enumerate(cells):
            is_dead = cell.choose_direction()
            if is_dead:
                dead_pool.append(cell)

        # kill all of the starved cells
        for cell in dead_pool:
            cell.die()

        # add food if needed
        if loop_counter % C.DROPPING_PACE == 0:
            BOARD.spread_food(food_dropped)

        # catching events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # translating mouse position into rows and columns
                col = pos[0] // (C.TILE_WIDTH + C.TILE_MARGIN)
                row = pos[1] // (C.TILE_HEIGHT + C.TILE_MARGIN)
                if BOARD.Grid[col][row].type == TileType.Grass:
                    t_rex = Cell("t_rex", 100000, col, row,
                                 15, C.INIT_HUNGER, 15, C.BLACK)
                    BOARD.num_cells += 1
                    BOARD.Grid[col][row] = t_rex
                print(str(row) + ", " + str(col))
                # print stuff that inhabits that square
                print(str(BOARD.Grid[col][row].name))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game_speed > 0:
                        game_speed -= 1
                    print("game speed: ", game_speed)
                if event.key == pygame.K_RIGHT:
                    if game_speed < C.MAX_GAME_SPEED:
                        game_speed += 1
                    print("game speed: ", game_speed)
                if event.key == pygame.K_UP:
                    food_dropped += 1
                    print("food dropped: ", food_dropped)
                if event.key == pygame.K_DOWN:
                    if food_dropped > 0:
                        food_dropped -= 1
                    print("food dropped: ", food_dropped)

        # print the grid
        color = C.BLACK
        SCREEN.fill(color)
        for row in range(C.MAP_SIZE):
            for col in range(C.MAP_SIZE):
                curr_tile = BOARD.Grid[col][row]
                is_cell = False
                if curr_tile.type == TileType.Grass:
                    color = C.GRASS
                if curr_tile.type == TileType.Cell:
                    is_cell = True
                    color = curr_tile.color if curr_tile.color else get_color_by_features(curr_tile)
                if curr_tile.type == TileType.Food:
                    color = C.FOOD_COLOR

                # location of the top left pixel of the MapTile
                row_start = (C.TILE_MARGIN + C.TILE_WIDTH) * col + C.TILE_MARGIN
                col_start = (C.TILE_MARGIN + C.TILE_HEIGHT) * row + C.TILE_MARGIN

                if is_cell:
                    pygame.draw.rect(
                        SCREEN,
                        C.WHITE,
                        [
                            row_start,
                            col_start,
                            C.TILE_WIDTH,
                            C.TILE_HEIGHT
                        ]
                    )
                    cell_percentage = size_to_percentage(curr_tile.size)
                    pygame.draw.circle(
                        SCREEN,
                        color,
                        [
                            int(row_start + C.TILE_WIDTH/2),
                            int(col_start + C.TILE_HEIGHT/2),
                        ],
                        int(C.TILE_WIDTH*cell_percentage/2)
                    )
                else:
                    pygame.draw.rect(
                        SCREEN,
                        color,
                        [
                            row_start,
                            col_start,
                            C.TILE_WIDTH,
                            C.TILE_HEIGHT
                        ]
                    )

        CLOCK.tick(60)      # Limit to 60 fps or something

        # Honestly not sure what this does, but it breaks if I remove it
        pygame.display.flip()

def get_color_by_features(cell: Cell):
    return (
        int(cell.size*25),
        int(cell.sight*25),
        int((C.MAX_FOOD_TO_REPRO - cell.food_to_repro + 1)*2.5*25)
        )

BOARD.spread_food(C.FOOD_DROPPED * 2)
run_game()
pygame.quit()
