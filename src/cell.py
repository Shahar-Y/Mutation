from pixel import Pixel
from enums import Step, CFeatures, PixelType


class Cell(Pixel):
    def __init__(self, speed, sight, replication, food, mutation_rate, health):
        super(Cell, self).__init__(1, 1)
        self.type = PixelType.Cell
        self.speed = speed
        self.sight = sight
        self.replication = replication
        self.food = food
        self.mutation_rate = mutation_rate
        self.health = health

    def __str__(self):
        return str("\n*******************************" +
                   print_fields(self) +
                   "\n*******************************")

    def step(self, step):
        self.x += step.value[0]
        self.y += step.value[1]

    def mutate(self, attr):
        if attr == CFeatures.FOOD:
            self.food += 1
        elif attr == CFeatures.HEALTH:
            self.health += 1
        elif attr == CFeatures.MU_RATE:
            self.mutation_rate += 1
        elif attr == CFeatures.REPLICATION:
            self.replication += 1
        elif attr == CFeatures.SIGHT:
            self.sight += 1
        elif attr == CFeatures.SPEED:
            self.speed += 1


def print_fields(cell):
    ret = ""
    for attr, value in vars(cell).items():
        ret += "\n" + str(attr) + ": " + str(value)
    return str(ret)
