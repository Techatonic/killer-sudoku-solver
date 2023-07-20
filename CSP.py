from Cage import parse_cage, Cage
from Cell import Cell
from helper import generate_killer_combinations
from constraint import AllDifferentConstraint, Problem, ExactSumConstraint

combinations = generate_killer_combinations()


def parse_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = Cell(i, j, board[i][j])
    return board


def parse_cages(input_cages):
    cages = []
    for cage in input_cages:
        cage = Cell(parse_cage(cage['first']), parse_cage(cage['second']))
        cages.append(Cage(cage.row, cage.col))

    return cages


class Sudoku:
    def __init__(self, grid, cages, filled_grid=None):
        self.board: list[list[Cell]] = parse_board(grid)
        self.cages: list[Cage] = parse_cages(cages)
        self.filled_grid = None if filled_grid is None else parse_board(filled_grid)

    def print_board(self):
        string = ""
        for i, row in enumerate(self.board):
            if i in [3, 6]:
                string += '------+-------+------\n'
            for j, col in enumerate(self.board[i]):
                if j in [3, 6]:
                    string += '|'
                string += str(self.board[i][j].val)
            string += "\n"
        print(string)
        return string

    def __repr__(self):
        return self.__str__()

    def evaluate_possibilities(self, possibilities, confirmed):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                val = self.board[row][col].val
                if val is None:
                    continue
                for other_row in range(len(self.board)):
                    if Cell(other_row, col) in possibilities:
                        possibilities[Cell(other_row, col)].discard(val)
                for other_col in range(len(self.board[row])):
                    if Cell(row, other_col) in possibilities:
                        possibilities[Cell(row, other_col)].discard(val)
                for other_row in range(row // 3, row // 3 + 3):
                    for other_col in range(col // 3, col // 3 + 3):
                        if Cell(other_row, other_col) in possibilities:
                            possibilities[Cell(other_row, other_col)].discard(val)
        return possibilities

    def convert_tuple_to_string(self, lst):
        return ''.join([str(i) for i in lst])

    def convert_string_to_tuple(self, string):
        return tuple([int(i) for i in string])

    def solve(self):
        possibilities = {}
        # Set initial possibilities
        for cage in self.cages:
            for cell in cage.cells:
                possibilities[self.convert_tuple_to_string((cell.row, cell.col))] = set().union(
                    *combinations[cage.length][cage.total])

        csp = Problem()

        for row in range(9):
            for col in range(9):
                domain = []
                for possibility in possibilities[self.convert_tuple_to_string((row, col))]:
                    domain.append(possibility)
                csp.addVariable(self.convert_tuple_to_string((row, col)), domain)

        for row in range(9):
            csp.addConstraint(AllDifferentConstraint(), [self.convert_tuple_to_string((row, i)) for i in range(9)])
        for col in range(9):
            csp.addConstraint(AllDifferentConstraint(), [self.convert_tuple_to_string((i, col)) for i in range(9)])
        for row in range(3):
            for col in range(3):
                box = []
                for i in range(3 * row, 3 * (row + 1)):
                    for j in range(3 * col, 3 * (col + 1)):
                        box.append(self.convert_tuple_to_string((i, j)))
                csp.addConstraint(AllDifferentConstraint(), box)

        for cage in self.cages:
            csp.addConstraint(ExactSumConstraint(cage.total),
                              [self.convert_tuple_to_string((cell.row, cell.col)) for cell in cage.cells])

        solutions = csp.getSolutions()

        if len(solutions) > 1:
            return False

        solution = solutions[0]

        for cell in solution:
            val = solution[cell]
            tup = self.convert_string_to_tuple(cell)
            cell = Cell(tup[0], tup[1], val)
            self.board[cell.row][cell.col] = cell

        # self.print_board()

        return True
