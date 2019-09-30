# Code source: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
import os
import pygame
import constants as C
from board import Board, Food, Cell

pygame.init()

WIN = pygame.display.set_mode((C.BORDERS, C.BORDERS))
# img = Image.open(os.path.join(os.getcwd(), 'src/images/cell.png'))
# basewidth = 20
# wpercent = (basewidth/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
# img = img.resize((basewidth,hsize), Image.ANTIALIAS)
# img.save(os.path.join(os.getcwd(), 'src/newUI/images/cell.png'))

WALK_RIGHT = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
WALK_LEFT = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
BG = pygame.image.load(os.path.join(os.getcwd(), 'src/images/water2.png'))
CHAR = pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))
CLOCK = pygame.time.Clock()


def redraw_game_window():
    WIN.blit(BG, (0, 0))
    for _, food in enumerate(FOODS):
        food.draw(WIN)
    for _, cell in enumerate(CELLS):
        cell.draw(WIN)
    pygame.display.update()

BOARD = Board(50)
FOODS = [Food(100, 100)]
CELLS = []
for _ in range(C.INIT_NUM_CELLS):
    CELLS.append(Cell(500, 500, 20, 20, CHAR))


#mainloop
RUN = True
while RUN:
    CLOCK.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    KEYS = pygame.key.get_pressed()
    for _, cell in enumerate(CELLS):
        cell.move(FOODS)
        cell.check_collision(FOODS[0])

    if KEYS[pygame.K_LEFT] and CELLS[0].x > 0:
        CELLS[0].x -= CELLS[0].vel
    if KEYS[pygame.K_RIGHT] and CELLS[0].x < C.BORDERS - CELLS[0].width:
        CELLS[0].x += CELLS[0].vel
    if KEYS[pygame.K_UP] and CELLS[0].y > 0:
        CELLS[0].y -= CELLS[0].vel
    if KEYS[pygame.K_DOWN] and CELLS[0].y < C.BORDERS - CELLS[0].height:
        CELLS[0].y += CELLS[0].vel

    redraw_game_window()

pygame.quit()
