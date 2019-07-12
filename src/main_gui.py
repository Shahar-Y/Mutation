import random as random
import pygame as pygame
from typing import List
from enums import TileType
import time

pygame.init()                                 # start up dat pygame
clock = pygame.time.Clock()                   # for frame-rate or something? still not very sure
Screen = pygame.display.set_mode([1000, 1000])  # making the window
Done = False                                  # variable to keep track if window is open
MapSize = 25                                  # how many tiles in either direction of grid

TileWidth = 20                                # pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

BLACK = (0, 0, 0)                             # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE3 = (0, 50, 250)
BLUE2 = (0, 150, 250)
BLUE1 = (0, 220, 250)


# The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
class MapTile(object):
    def __init__(self, name, column, row, tile_type):
        self.Type = tile_type
        self.Name = name
        self.Column = column
        self.Row = row


# Characters can move around and do cool stuff
class Character(object):
    def __init__(self, name, hp, column, row):
        self.Name = name
        self.HP = hp
        self.Column = column
        self.Row = row

    def handle_step(self, col_advance, row_advance):
        new_col = self.Column + col_advance
        new_row = self.Row + row_advance
        if Map.Grid[new_col][new_row].Type == TileType.Food:
            self.HP += 10
            Map.NumFood -= 1
            if self.HP >= 30:
                print("reproducing!")
                self.HP = 0
                self.reproduce()
            print("new HP: {}".format(self.HP))

        if Map.Grid[new_col][new_row].Type == TileType.Grass or Map.Grid[new_col][new_row].Type == TileType.Food:
            Map.Grid[self.Column][self.Row] = MapTile("Grass", self.Column, self.Row, TileType.Grass)
            self.Row += row_advance
            self.Column += col_advance
            Map.Grid[self.Column][self.Row] = MapTile(self.Name, self.Column, self.Row, TileType.Cell)

    # This function is how a character moves around in a certain direction
    def move(self, direction):

        if direction == "UP":
            if self.Row > 0 and not(self.collides("UP")):
                self.handle_step(0, -1)

        elif direction == "LEFT":
            if self.Column > 0 and not(self.collides("LEFT")):
                self.handle_step(-1, 0)

        elif direction == "RIGHT":
            if self.Column < MapSize-1 and not(self.collides("RIGHT")):
                self.handle_step(1, 0)

        elif direction == "DOWN":
            if self.Row < MapSize-1 and not(self.collides("DOWN")):
                self.handle_step(0, 1)

    # Checks if anything is on top of the grass in the direction that the character wants to move.
    # Used in the move function
    def collides(self, direction):
        if direction == "UP":
            if (Map.Grid[self.Column][self.Row-1]).Type == TileType.Rock:
                return True
        elif direction == "LEFT":
            if (Map.Grid[self.Column-1][self.Row]).Type == TileType.Rock:
                return True
        elif direction == "RIGHT":
            if (Map.Grid[self.Column+1][self.Row]).Type == TileType.Rock:
                return True
        elif direction == "DOWN":
            if (Map.Grid[self.Column][self.Row+1]).Type == TileType.Rock:
                return True
        return False

    def reproduce(self):
        col, row = self.adjasent_free_space()
        new_cell = Character("Hero", 0, col, row)
        Map.Grid[col][row] = MapTile("cell" + str(Map.index), col, row, TileType.Cell)
        Map.index += 1
        Map.Cells.append(new_cell)

    def adjasent_free_space(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not(i == j and i == 0):
                    if Map.Grid[self.Column + i][self.Row + j].Type == TileType.Grass:
                        return self.Column + i, self.Row + j


# The main class; where the action happens
class Map(object):
    global MapSize

    index = 1
    NumFood = 0
    Grid: List[List[MapTile]] = []*(MapSize*MapSize)

    empty_tile = MapTile("", 0, 0, TileType.Pixel)
    for Row in range(MapSize*MapSize):     # Creating grid
        Grid.append([empty_tile])
        for Column in range(MapSize):
            Grid[Row].append(empty_tile)

    for Row in range(MapSize):     # Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("Grass", Column, Row, TileType.Grass)
            Grid[Column][Row] = TempTile

    RandomColumn = random.randint(0, MapSize - 1)
    RandomRow = random.randint(0, MapSize - 1)
    Hero = Character("Hero", 0, RandomColumn, RandomRow)
    Cells: List[Character] = [Hero]
    Grid[RandomColumn][RandomRow] = MapTile("Hero", RandomColumn, RandomRow, TileType.Cell)

    def spread_food(self, num):
        for i in range(num):
            while True:
                rand_col = random.randint(0, MapSize - 1)
                rand_row = random.randint(0, MapSize - 1)
                if self.Grid[rand_col][rand_row].Type == TileType.Grass:
                    temp_tile = MapTile("Food", rand_col, rand_row, TileType.Food)
                    self.Grid[rand_col][rand_row] = temp_tile
                    self.NumFood += 1
                    break


Map = Map()
Map.spread_food(150)


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
        if Map.Cells[i].Column == col and Map.Cells[i].Row == row:
            return i

def run_game():
    done = False
    while not done:     # Main pygame loop
        time.sleep(0.1)
        for i in range(len(Map.Cells)):
            num = random.randint(0, 3)
            Map.Cells[i].move(int_to_direction(num))

        if Map.NumFood <= 20:
            Map.spread_food(20)

        for event in pygame.event.get():         # catching events
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (TileWidth + TileMargin)  # Translating mouse position into rows and columns
                row = pos[1] // (TileHeight + TileMargin)
                print(str(row) + ", " + str(column))
                print(str(Map.Grid[column][row].Name))  # print stuff that inhabits that square

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
        Screen.fill(color)
        for Row in range(MapSize):           # Drawing grid
            for Column in range(MapSize):
                if Map.Grid[Column][Row].Type == TileType.Grass:
                    color = WHITE
                if Map.Grid[Column][Row].Type == TileType.Cell:
                    index = get_cells_by_location(Column, Row)
                    if Map.Cells[index].HP <= 0:
                        color = BLUE1
                    elif Map.Cells[index].HP <= 10:
                        color = BLUE2
                    elif Map.Cells[index].HP <= 20:
                        color = BLUE3
                if Map.Grid[Column][Row].Type == TileType.Food:
                    color = RED

                pygame.draw.rect(Screen, color, [(TileMargin + TileWidth) * Column + TileMargin,
                                                 (TileMargin + TileHeight) * Row + TileMargin,
                                                 TileWidth,
                                                 TileHeight])

        clock.tick(60)      # Limit to 60 fps or something

        pygame.display.flip()     # Honestly not sure what this does, but it breaks if I remove it


run_game()
pygame.quit()