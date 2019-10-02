import os
import random
import pygame
import constants as C
from new_board import Board, Cell
import cv2

image = cv2.imread("src/newUI/images/original_cell.png")
overlay = image.copy()
output = image.copy()
cv2.circle(overlay, (125, 125), 115, (0, 255, 255), -1)
alpha = 0.5
cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
file_name = 'src/images/Output'+str(alpha) +'.jpg'
cv2.imwrite(file_name, output)
cv2.waitKey(0)
cv2.destroyAllWindows()

src = cv2.imread(file_name, 1)
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_,alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
b, g, r = cv2.split(src)
rgba = [b,g,r, alpha]
dst = cv2.merge(rgba, 4)
dst = cv2.resize(dst, (0,0), fx=0.1, fy=0.1)
cv2.imwrite('src/newUI/images/new_cell.png', dst)

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
CHAR = pygame.image.load(os.path.join(os.getcwd(), 'src/newUI/images/new_cell.png'))
CLOCK = pygame.time.Clock()


def redraw_game_window():
    WIN.blit(BG, (0, 0))
    for _, food in enumerate(BOARD.foods):
        food.draw(WIN)
    for cell in BOARD.cells:
        cell.draw(WIN)
    pygame.display.update()

BOARD = Board()
BOARD.foods = []
BOARD.cells = []
for _ in range(C.INIT_NUM_CELLS):
    BOARD.cells.append(Cell(500, 500, 20, 20, CHAR, C.INIT_HUNGER))


#mainloop
RUN = True
ITERATIONS = 0
while RUN:
    ITERATIONS += 1
    CLOCK.tick(25)
    if ITERATIONS % C.DROPPING_PACE == 0:
        for i in range(1, 10):
            BOARD.add_food(random.randint(0, C.WINDOW_SIZE), random.randint(0, C.WINDOW_SIZE))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    KEYS = pygame.key.get_pressed()
    BOARD.make_step()


    if KEYS[pygame.K_LEFT] and BOARD.cells[0].x > 0:
        BOARD.cells[0].x -= BOARD.cells[0].vel
    if KEYS[pygame.K_RIGHT] and BOARD.cells[0].x < C.BORDERS - BOARD.cells[0].width:
        BOARD.cells[0].x += BOARD.cells[0].vel
    if KEYS[pygame.K_UP] and BOARD.cells[0].y > 0:
        BOARD.cells[0].y -= BOARD.cells[0].vel
    if KEYS[pygame.K_DOWN] and BOARD.cells[0].y < C.BORDERS - BOARD.cells[0].height:
        BOARD.cells[0].y += BOARD.cells[0].vel

    redraw_game_window()

pygame.quit()
