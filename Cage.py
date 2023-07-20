from Cell import Cell


class Cage:
    def __init__(self, total, cells):
        self.total = total
        self.length = len(cells)
        self.cells = cells

    def __str__(self):
        return f'\nLength: {self.length}\tTotal: {self.total}\tCells: {self.cells}\n'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.cells == other.cells

    def __hash__(self):
        return hash(tuple([self.total, self.length, hash(tuple(self.cells))]))


def parse_cage(cage):
    if type(cage) == dict:
        return Cell(parse_cage(cage['first']), parse_cage(cage['second']))
    if type(cage) == list:
        return [parse_cage(i) for i in cage]
    return cage
