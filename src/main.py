from cell import Cell
from enums import Step, CFeatures

def main():
    celly = Cell(0, 0, 3, 4, 5, 6)
    print(celly)
    celly.step(Step.RIGHT)
    print(celly)
    celly.mutate(CFeatures.SPEED)
    print(celly)

main()
