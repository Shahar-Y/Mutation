from typing import List
import random
from enums import TileType
import constants as C
from map_tile import MapTile

# cells can move around and do cool stuff

def get_rand_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Cell(MapTile):
    def __init__(self, name, food_to_repro, col, row, size, hunger, sight, color):
        MapTile.__init__(self, name, col, row, TileType.Cell)
        self.pregnancy = 0
        self.hunger = hunger
        self.food_worth = C.FOOD_WORTH
        self.is_dead = False
        self.color = color
        self.times_replicated = 0
        # The three mutateable features of a cell
        self.food_to_repro = food_to_repro
        self.sight = sight
        self.size = size

    def food_eaten(self):
        self.pregnancy += 1
        if self.hunger - C.FOOD_WORTH >= 0:
            self.hunger = self.hunger - C.FOOD_WORTH
        else:
            self.hunger = 0
        BOARD.num_food -= 1
        if self.pregnancy >= self.food_to_repro:
            self.pregnancy = 0
            self.reproduce()


    def handle_step(self, col_advance, row_advance):
        new_col = self.col + col_advance
        new_row = self.row + row_advance
        curr_tile = BOARD.Grid[new_col][new_row]
        if curr_tile.type == TileType.Food:
            self.food_eaten()

        if curr_tile.type == TileType.Cell and self.size >= curr_tile.size+C.EATING_SIZE:
            # print(self.col, ", ", self.row, " eating cell in ", new_col, ", ", new_row)
            curr_tile.is_dead = True
            self.food_eaten()
            # print("done")

        if curr_tile.type == TileType.Grass or curr_tile.type == TileType.Food:
            BOARD.Grid[self.col][self.row] = MapTile(
                "Grass", self.col, self.row, TileType.Grass)
            self.col = new_col
            self.row = new_row
            BOARD.Grid[new_col][new_row] = self
        self.hunger += 1
        if(self.hunger) >= 100:
            return True
        return False

    # This function is how a cell moves around in a certain direction
    def move(self, direction):
        is_dead = False
        if direction == "UP":
            if self.row > 0 and not self.collides("UP"):
                is_dead = self.handle_step(0, -1)

        elif direction == "LEFT":
            if self.col > 0 and not self.collides("LEFT"):
                is_dead = self.handle_step(-1, 0)

        elif direction == "RIGHT":
            if self.col < C.MAP_SIZE-1 and not self.collides("RIGHT"):
                is_dead = self.handle_step(1, 0)

        elif direction == "DOWN":
            if self.row < C.MAP_SIZE-1 and not self.collides("DOWN"):
                is_dead = self.handle_step(0, 1)
        return is_dead

    def choose_direction(self):
        if self.is_dead:
            return True
        # search for food in sight
        for i in range(0, self.sight+1):
            array = get_close_array(i)
            random.shuffle(array)
            for index in array:
                if has_food(self, self.col + index[0], self.row + index[1]):
                    return self.move(get_directions(index[0], index[1]))

        # If the cell doesn't see food:
        num = random.randint(0, 3)
        return self.move(int_to_direction(num))

    # Checks if anything is on top of the grass in the direction that the cell wants to move.
    # Used in the move function

    def collides(self, direction):
        if direction == "UP":
            if (BOARD.Grid[self.col][self.row-1]).type == TileType.Rock:
                return True
        elif direction == "LEFT":
            if (BOARD.Grid[self.col-1][self.row]).type == TileType.Rock:
                return True
        elif direction == "RIGHT":
            if (BOARD.Grid[self.col+1][self.row]).type == TileType.Rock:
                return True
        elif direction == "DOWN":
            if (BOARD.Grid[self.col][self.row+1]).type == TileType.Rock:
                return True
        return False

    def die(self):
        BOARD.Grid[self.col][self.row] = MapTile(
            "Grass", self.col, self.row, TileType.Grass)
        BOARD.num_cells -= 1
        BOARD.total_died += 1
        del self

    def reproduce(self):
        col, row = self.adjasent_free_space()

        self.hunger = int(100-(100-self.hunger)/2)
        new_cell = Cell("cell" + str(Map.index), self.food_to_repro,
                        col, row, self.size, self.hunger, self.sight, self.color)
        if random.randint(1, C.MUTATION_CHANCE) == 1:
            new_cell.mutate_properties()
        BOARD.Grid[col][row] = new_cell
        BOARD.index += 1
        BOARD.num_cells += 1
        BOARD.total_lived += 1

    def adjasent_free_space(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not(i == j and i == 0):
                    if BOARD.Grid[self.col + i][self.row + j].type == TileType.Grass:
                        return self.col + i, self.row + j
        return -1, -1

    def mutate_properties(self):
        switcher = {
            0: get_sight(self),
            1: get_size(self),
            2: get_food_to_repro(self),
        }
        while True:
            prop_inc = random.randint(0, 2)
            prop_dec = random.randint(0, 2)
            if prop_inc == prop_dec:
                continue
            inc_curr_value, inc_max, inc_min, inc_name, v_1 = switcher.get(prop_inc, "Invalid inc")
            dec_curr_value, dec_max, dec_min, dec_name, v_2 = switcher.get(prop_dec, "Invalid dec")
            if (inc_curr_value + v_2 > inc_max or inc_curr_value + v_2 < inc_min
                    or dec_curr_value - v_1 > dec_max or dec_curr_value - v_1 < dec_min):
                continue
            self.__setattr__(inc_name, self.__getattribute__(inc_name) + v_2)
            self.__setattr__(dec_name, self.__getattribute__(dec_name) - v_1)
            break

def get_sight(cell: Cell):
    return cell.sight, C.MAX_SIGHT, C.MIN_SIGHT, "sight", 1

def get_size(cell: Cell):
    return cell.size, C.MAX_SIZE, C.MIN_SIZE, "size", 1

def get_food_to_repro(cell: Cell):
    return cell.food_to_repro, C.MAX_FOOD_TO_REPRO, C.MIN_FOOD_TO_REPRO, "food_to_repro", -2


# The main class; where the action happens
class Map(object):
    total_lived = 0
    total_died = 0
    index = 1
    num_food = 0
    num_cells = 0
    Grid: List[List[MapTile]] = []*(C.MAP_SIZE*C.MAP_SIZE)

    empty_tile = MapTile("", 0, 0, TileType.Pixel)
    for row in range(C.MAP_SIZE*C.MAP_SIZE):     # Creating grid
        Grid.append([empty_tile])
        for Column in range(C.MAP_SIZE):
            Grid[row].append(empty_tile)

    for row in range(C.MAP_SIZE):     # Filling grid with grass
        for Column in range(C.MAP_SIZE):
            TempTile = MapTile("Grass", Column, row, TileType.Grass)
            Grid[Column][row] = TempTile

    RandomColumn = random.randint(0, C.MAP_SIZE - 1)
    RandomRow = random.randint(0, C.MAP_SIZE - 1)
    Hero = Cell("Hero", C.INIT_FOOD_TO_REPRO, RandomColumn, RandomRow,
                C.INIT_SIZE, C.INIT_HUNGER, C.INIT_SIGHT, 0)
    total_lived += 1
    num_cells += 1
    Grid[RandomColumn][RandomRow] = Hero

    def spread_food(self, num):
        for _ in range(num):
            tries = 0
            while tries < 100:
                tries += 1
                rand_col = random.randint(0, C.MAP_SIZE - 1)
                rand_row = random.randint(0, C.MAP_SIZE - 1)
                if self.Grid[rand_col][rand_row].type == TileType.Grass:
                    temp_tile = MapTile(
                        "Food", rand_col, rand_row, TileType.Food)
                    self.Grid[rand_col][rand_row] = temp_tile
                    self.num_food += 1
                    break


def get_close_array(sight):
    array = []
    if sight == 0:
        return array
    for i in range(0, sight+1):
        col = i
        row = sight-i
        array.append([col, row])
        array.append([-col, -row])
        if col != 0 and row != 0:
            array.append([-col, row])
            array.append([col, -row])
    return array


def has_food(cell, col, row):
    if col >= 0 and col < C.MAP_SIZE and row >= 0 and row <= C.MAP_SIZE:
        if ((BOARD.Grid[col][row].type == TileType.Food)
                or (BOARD.Grid[col][row].type == TileType.Cell
                    and cell.size - BOARD.Grid[col][row].size >= C.EATING_SIZE)):
            return True
    return False


def get_directions(col_step, row_step):
    if col_step < 0:
        return "LEFT"
    elif row_step < 0:
        return "UP"
    elif col_step > 0:
        return "RIGHT"
    elif row_step > 0:
        return "DOWN"
    return "DOWN"


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


BOARD = Map()
