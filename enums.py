from enum import Enum, auto


class PixelType(Enum):
    Pixel = auto()
    Cell = auto()
    Food = auto()
    Rock = auto()
    Antibiotics = auto()


class Step(Enum):
    RIGHT = [1, 0]
    LEFT = [-1, 0]
    UP = [0, 1]
    DOWN = [0, -1]


class CFeatures:
    SPEED = auto()
    SIGHT = auto()
    REPLICATION = auto()
    FOOD = auto()
    MU_RATE = auto()
    HEALTH = auto()