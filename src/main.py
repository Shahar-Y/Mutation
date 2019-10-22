import os
import random
import pygame
import constants as C
from board import Board, Cell
# from new_db import resize_food, create_db


# file_name = 'src/images/icons/Cell_10_10_2.png'
pygame.init()

WIN = pygame.display.set_mode((C.WINDOW_WIDTH, C.WINDOW_HEIGHT))

# WALK_RIGHT = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
# WALK_LEFT = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
BG = pygame.image.load(os.path.join(os.getcwd(), 'src/images/water2.png'))
# CHAR = pygame.image.load(os.path.join(os.getcwd(), file_name))
CLOCK = pygame.time.Clock()


def redraw_game_window():
    WIN.blit(BG, (0, 0))
    for _, food in enumerate(BOARD.foods):
        food.draw(WIN)
    for cell in BOARD.cells:
        cell.draw(WIN)
    pygame.display.update()

BOARD = Board()

for _ in range(C.INIT_NUM_CELLS):
    BOARD.cells.append(Cell(500, 500, C.INIT_HUNGER, C.INIT_SIZE,
                            C.INIT_SIGHT, C.INIT_VEL))


#mainloop
RUN = True
ITERATIONS = 0
while RUN:
    CLOCK.tick(C.GAME_SPEED)
    if ITERATIONS % C.DROPPING_PACE == 0 and len(BOARD.foods) <= C.MAX_FOOD_ON_BOARD:
        for i in range(1, C.FOOD_DROPPED):
            BOARD.add_food(random.randint(5, C.WINDOW_WIDTH), random.randint(5, C.WINDOW_HEIGHT))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    KEYS = pygame.key.get_pressed()
    BOARD.make_step()
    ITERATIONS += 1


    if KEYS[pygame.K_LEFT] and BOARD.cells[0].x > 0:
        BOARD.cells[0].x -= BOARD.cells[0].vel
    if KEYS[pygame.K_RIGHT] and BOARD.cells[0].x < C.WINDOW_WIDTH - BOARD.cells[0].width:
        BOARD.cells[0].x += BOARD.cells[0].vel
    if KEYS[pygame.K_UP] and BOARD.cells[0].y > 0:
        BOARD.cells[0].y -= BOARD.cells[0].vel
    if KEYS[pygame.K_DOWN] and BOARD.cells[0].y < C.WINDOW_HEIGHT - BOARD.cells[0].height:
        BOARD.cells[0].y += BOARD.cells[0].vel

    redraw_game_window()

pygame.quit()
