from typing import List
import random
import time
import pygame
from enums import TileType

pygame.init()                                 # start up dat pygame
CLOCK = pygame.time.Clock()                   # for frame-rate or something? still not very sure
DONE = False                                  # variable to keep track if window is open
MAP_SIZE = 30                                  # how many tiles in either direction of grid

TILE_WIDTH = 18                                # pixel sizes for grid squares
TILE_HEIGHT = TILE_WIDTH
TILE_MARGIN = 4

FOOD_DROPPED = int(MAP_SIZE*MAP_SIZE / 5)

WINDOW_SIZE = (TILE_WIDTH + TILE_MARGIN) * MAP_SIZE + TILE_MARGIN
SCREEN = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])  # making the window

INIT_HUNGER = 80
FOOD_WORTH = 10

BLACK = (0, 0, 0)                             # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRASS = (255, 255, 255)
RED = GREEN
BLUE = (0, 0, 255)
BLUE3 = (0, 50, 250)
BLUE2 = (0, 150, 250)
BLUE1 = (0, 220, 250)


# The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
class MapTile():
    def __init__(self, name, column, row, tile_type):
        self.type = tile_type
        self.name = name
        self.column = column
        self.row = row


# Characters can move around and do cool stuff
class Character(object):
    def __init__(self, name, hp, column, row):
        self.name = name
        self.health = hp
        self.column = column
        self.row = row
        self.hunger = INIT_HUNGER

    def handle_step(self, col_advance, row_advance):
        new_col = self.column + col_advance
        new_row = self.row + row_advance
        curr_tile = Map.Grid[new_col][new_row]
        if curr_tile.type == TileType.Food:
            self.health += 10
            if self.hunger - FOOD_WORTH >= 0:
                self.hunger = self.hunger - FOOD_WORTH
            else:
                self.hunger = 0
            Map.num_food -= 1
            if self.health >= 30:
                self.health = 0
                self.reproduce()

        if curr_tile.type == TileType.Grass or curr_tile.type == TileType.Food:
            Map.Grid[self.column][self.row] = MapTile("Grass", self.column, self.row, TileType.Grass)
            self.column = new_col
            self.row = new_row
            Map.Grid[self.column][self.row] = MapTile(self.name, self.column, self.row, TileType.Cell)
        self.hunger += 1
        if(self.hunger) >= 100:
            return True
        return False

    # This function is how a character moves around in a certain direction
    def move(self, direction):
        is_dead = False
        if direction == "UP":
            if self.row > 0 and not self.collides("UP"):
                is_dead = self.handle_step(0, -1)

        elif direction == "LEFT":
            if self.column > 0 and not self.collides("LEFT"):
                is_dead = self.handle_step(-1, 0)

        elif direction == "RIGHT":
            if self.column < MAP_SIZE-1 and not self.collides("RIGHT"):
                is_dead = self.handle_step(1, 0)

        elif direction == "DOWN":
            if self.row < MAP_SIZE-1 and not self.collides("DOWN"):
                is_dead = self.handle_step(0, 1)
        return is_dead

    # Checks if anything is on top of the grass in the direction that the character wants to move.
    # Used in the move function
    def collides(self, direction):
        if direction == "UP":
            if (Map.Grid[self.column][self.row-1]).type == TileType.Rock:
                return True
        elif direction == "LEFT":
            if (Map.Grid[self.column-1][self.row]).type == TileType.Rock:
                return True
        elif direction == "RIGHT":
            if (Map.Grid[self.column+1][self.row]).type == TileType.Rock:
                return True
        elif direction == "DOWN":
            if (Map.Grid[self.column][self.row+1]).type == TileType.Rock:
                return True
        return False

    def die(self):
        print('DYING :(')
        Map.Grid[self.column][self.row] = MapTile("Grass", self.column, self.row, TileType.Grass)
        Map.Cells.remove(self)
        del self

    def reproduce(self):
        col, row = self.adjasent_free_space()
        if col < 0:
            return
        print("reproducing!")
        new_cell = Character("Hero", 0, col, row)
        Map.Grid[col][row] = MapTile("cell" + str(Map.index), col, row, TileType.Cell)
        Map.index += 1
        Map.Cells.append(new_cell)

    def adjasent_free_space(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not(i == j and i == 0):
                    if Map.Grid[self.column + i][self.row + j].type == TileType.Grass:
                        return self.column + i, self.row + j
        return -1, -1


# The main class; where the action happens
class Map(object):
    global MAP_SIZE

    index = 1
    num_food = 0
    Grid: List[List[MapTile]] = []*(MAP_SIZE*MAP_SIZE)

    empty_tile = MapTile("", 0, 0, TileType.Pixel)
    for row in range(MAP_SIZE*MAP_SIZE):     # Creating grid
        Grid.append([empty_tile])
        for Column in range(MAP_SIZE):
            Grid[row].append(empty_tile)

    for row in range(MAP_SIZE):     # Filling grid with grass
        for Column in range(MAP_SIZE):
            TempTile = MapTile("Grass", Column, row, TileType.Grass)
            Grid[Column][row] = TempTile

    RandomColumn = random.randint(0, MAP_SIZE - 1)
    RandomRow = random.randint(0, MAP_SIZE - 1)
    Hero = Character("Hero", 0, RandomColumn, RandomRow)
    Cells: List[Character] = [Hero]
    Grid[RandomColumn][RandomRow] = MapTile("Hero", RandomColumn, RandomRow, TileType.Cell)

    def spread_food(self, num):
        for i in range(num):
            tries = 0
            while tries < 100:
                tries += 1
                rand_col = random.randint(0, MAP_SIZE - 1)
                rand_row = random.randint(0, MAP_SIZE - 1)
                if self.Grid[rand_col][rand_row].type == TileType.Grass:
                    temp_tile = MapTile("Food", rand_col, rand_row, TileType.Food)
                    self.Grid[rand_col][rand_row] = temp_tile
                    self.num_food += 1
                    break


Map = Map()
Map.spread_food(FOOD_DROPPED * 2)


def int_to_direction(num):
    if num % 4 == 0:
        return "LEFT"
    if num % 4 == 1:
        return "RIGHT"
    if num % 4 == 2:
        return "UP"
    if num % 4 == 3:
        return "DOWN"

def get_cells_by_location(col, row):
    for i in range(len(Map.Cells)):
        if Map.Cells[i].column == col and Map.Cells[i].row == row:
            return i

def run_game():
    done = False
    while not done:     # Main pygame loop
        time.sleep(0.1)
        dead_pool: List[Character] = []
        for i in range(len(Map.Cells)):
            num = random.randint(0, 3)
            is_dead = Map.Cells[i].move(int_to_direction(num))
            if is_dead:
                dead_pool.append(Map.Cells[i])

        for cell in dead_pool:
            cell.die()

        if Map.num_food <= FOOD_DROPPED:
            Map.spread_food(FOOD_DROPPED)

        for event in pygame.event.get():         # catching events
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (TILE_WIDTH + TILE_MARGIN)  # Translating mouse position into rows and columns
                row = pos[1] // (TILE_HEIGHT + TILE_MARGIN)
                print(str(row) + ", " + str(column))
                print(str(Map.Grid[column][row].name))  # print stuff that inhabits that square

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Map.Hero.move("LEFT")
                if event.key == pygame.K_RIGHT:
                    Map.Hero.move("RIGHT")
                if event.key == pygame.K_UP:
                    Map.Hero.move("UP")
                if event.key == pygame.K_DOWN:
                    Map.Hero.move("DOWN")

        color = BLACK
        SCREEN.fill(color)
        for row in range(MAP_SIZE):           # Drawing grid
            for Column in range(MAP_SIZE):
                if Map.Grid[Column][row].type == TileType.Grass:
                    color = GRASS
                if Map.Grid[Column][row].type == TileType.Cell:
                    index = get_cells_by_location(Column, row)
                    if Map.Cells[index].health <= 0:
                        color = BLUE1
                    elif Map.Cells[index].health <= 10:
                        color = BLUE2
                    elif Map.Cells[index].health <= 20:
                        color = BLUE3
                if Map.Grid[Column][row].type == TileType.Food:
                    color = RED

                pygame.draw.rect(SCREEN, color, [(TILE_MARGIN + TILE_WIDTH) * Column + TILE_MARGIN,
                                                 (TILE_MARGIN + TILE_HEIGHT) * row + TILE_MARGIN,
                                                 TILE_WIDTH,
                                                 TILE_HEIGHT])

        CLOCK.tick(60)      # Limit to 60 fps or something

        pygame.display.flip()     # Honestly not sure what this does, but it breaks if I remove it


run_game()
pygame.quit()