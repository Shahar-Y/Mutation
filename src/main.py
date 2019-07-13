from typing import List
import random
import time
import pygame
from enums import TileType
import constants as C
from board import Character, BOARD

pygame.init()                                 # start up dat pygame
CLOCK = pygame.time.Clock()                   # for frame-rate or something? still not very sure
SCREEN = pygame.display.set_mode([C.WINDOW_SIZE, C.WINDOW_SIZE])  # making the window

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

def get_cells_by_location(col, row):
    for i in range(len(BOARD.Cells)):
        if BOARD.Cells[i].col == col and BOARD.Cells[i].row == row:
            return i
    return -1


def run_game():
    done = False
    while not done:     # Main pygame loop
        time.sleep(0.1)
        dead_pool: List[Character] = []
        for i in range(len(BOARD.Cells)):
            num = random.randint(0, 3)
            is_dead = BOARD.Cells[i].move(int_to_direction(num))
            if is_dead:
                dead_pool.append(BOARD.Cells[i])

        for cell in dead_pool:
            cell.die()

        print('CHECKING: ' + str(BOARD.num_food) + ', ' + str(C.FOOD_DROPPED))
        if BOARD.num_food <= C.FOOD_DROPPED:
            print('SPREADING FOOD' + str(BOARD.num_food) + ', ' + str(C.FOOD_DROPPED))
            BOARD.spread_food(C.FOOD_DROPPED)

        for event in pygame.event.get():         # catching events
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // (C.TILE_WIDTH + C.TILE_MARGIN)  # Translating mouse position into rows and columns
                row = pos[1] // (C.TILE_HEIGHT + C.TILE_MARGIN)
                print(str(row) + ", " + str(col))
                print(str(BOARD.Grid[col][row].name))  # print stuff that inhabits that square

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    BOARD.Hero.move("LEFT")
                if event.key == pygame.K_RIGHT:
                    BOARD.Hero.move("RIGHT")
                if event.key == pygame.K_UP:
                    BOARD.Hero.move("UP")
                if event.key == pygame.K_DOWN:
                    BOARD.Hero.move("DOWN")

        color = C.BLACK
        SCREEN.fill(color)
        for row in range(C.MAP_SIZE):           # Drawing grid
            for col in range(C.MAP_SIZE):
                if BOARD.Grid[col][row].type == TileType.Grass:
                    color = C.GRASS
                if BOARD.Grid[col][row].type == TileType.Cell:
                    index = get_cells_by_location(col, row)
                    if index < 0:
                        print("BAD INDEX")
                        continue
                    if BOARD.Cells[index].health <= 0:
                        color = C.BLUE1
                    elif BOARD.Cells[index].health <= C.REPRO_HEALTH/3:
                        color = C.BLUE2
                    elif BOARD.Cells[index].health <= 2*C.REPRO_HEALTH/3:
                        color = C.BLUE3
                if BOARD.Grid[col][row].type == TileType.Food:
                    color = C.RED

                pygame.draw.rect(SCREEN, color, [(C.TILE_MARGIN + C.TILE_WIDTH) * col + C.TILE_MARGIN,
                                                 (C.TILE_MARGIN + C.TILE_HEIGHT) * row + C.TILE_MARGIN,
                                                 C.TILE_WIDTH,
                                                 C.TILE_HEIGHT])

        CLOCK.tick(60)      # Limit to 60 fps or something

        pygame.display.flip()     # Honestly not sure what this does, but it breaks if I remove it


BOARD.spread_food(C.FOOD_DROPPED * 2)
run_game()
pygame.quit()
