# THIS WAS FOR AN ALTERNATIVE SOLUTION. CURRENTLY THE CSP METHOD WORKS SO THIS IS NOT NECESSARY

# import copy
# import pprint
#
# from Cage import Cage, parse_cage
# from Cell import Cell
# from helper import generate_killer_combinations
#
# combinations = generate_killer_combinations()
#
#
# def parse_board(board):
#     for i in range(len(board)):
#         for j in range(len(board[i])):
#             board[i][j] = Cell(i, j, board[i][j])
#     return board
#
#
# def parse_cages(input_cages):
#     cages = []
#     for cage in input_cages:
#         cage = Cell(parse_cage(cage['first']), parse_cage(cage['second']))
#         cages.append(Cage(cage.row, cage.col))
#
#     return cages
#
#
# class KillerSudoku:
#     def __init__(self, grid, cages, filled_grid=None):
#         self.board: list[list[Cell]] = parse_board(grid)
#         self.cages: list[Cage] = parse_cages(cages)
#         self.filled_grid = None if filled_grid is None else parse_board(filled_grid)
#
#     def __str__(self):
#         string = ""
#         for i, row in enumerate(self.board):
#             if i in [3, 6]:
#                 string += '------+-------+------\n'
#             for j, col in enumerate(self.board[i]):
#                 if j in [3, 6]:
#                     string += '|'
#                 string += str(self.board[i][j].val)
#             string += "\n"
#         return string
#
#     def __repr__(self):
#         return self.__str__()
#
#     def evaluate_possibilities(self, possibilities, confirmed):
#         for row in range(len(self.board)):
#             for col in range(len(self.board[row])):
#                 val = self.board[row][col].val
#                 if val is None:
#                     continue
#                 for other_row in range(len(self.board)):
#                     if Cell(other_row, col) in possibilities:
#                         possibilities[Cell(other_row, col)].discard(val)
#                 for other_col in range(len(self.board[row])):
#                     if Cell(row, other_col) in possibilities:
#                         possibilities[Cell(row, other_col)].discard(val)
#                 for other_row in range(row // 3, row // 3 + 3):
#                     for other_col in range(col // 3, col // 3 + 3):
#                         if Cell(other_row, other_col) in possibilities:
#                             possibilities[Cell(other_row, other_col)].discard(val)
#         return possibilities
#
#     def is_possible(self, possibilities, confirmed) -> bool:
#         possibilities = self.evaluate_possibilities(possibilities, confirmed)
#         return all(len(possibilities[x]) > 0 for x in possibilities)
#
#     def solve(self):
#         possibilities = {}
#         confirmed = {}
#         # Set initial possibilities
#         for cage in self.cages:
#             for cell in cage.cells:
#                 possibilities[cell] = set().union(*combinations[cage.length][cage.total])
#
#
#         while True:
#             # Reevaluate possibilities
#             possibilities = self.evaluate_possibilities(possibilities, confirmed)
#
#             for cage in self.cages:
#                 for cell in cage.cells:
#                     possibilities[cell] = set().intersection(*[possibilities[cell]],
#                                                              set().union(*combinations[cage.length][cage.total]))
#
#
#             # pprint.pprint(possibilities)
#
#             # Assign value if cell has only one possibility
#             change_made = False
#             for cell in possibilities:
#                 if len(possibilities[cell]) == 1:
#                     print("Found")
#                     exit()
#                     confirmed[cell] = possibilities[cell][0]
#                     self.board[cell.row][cell.col] = possibilities[cell][0]
#                     # del possibilities[cell]
#
#                     change_made = True
#             if change_made:
#                 continue
#
#             # Replace cages with smaller cages if confirmed vals
#             for i in range(len(self.cages)):
#                 cage = self.cages[i]
#                 confirmed_cells = list(filter(lambda cell: cell.val is not None, cage.cells))
#                 if len(confirmed_cells) > 0:
#                     new_cage = Cage(cage.total - sum(cell.val for cell in confirmed_cells),
#                                     list(set(cage.cells)-set(confirmed_cells)))
#                     self.cages[i] = new_cage
#                     change_made = True
#
#                 # Handle single length cages
#                 if cage.length == 1:
#                     cell = cage.cells[0]
#                     confirmed[cell] = cage.total
#                     self.board[cell.row][cell.col].val = cage.total
#                     possibilities[cell] = {cage.total}
#                     # del possibilities[cell]
#                     del cage
#             if change_made:
#                 continue
#
#             # Cages cover all but one on row
#             temp_cages = copy.deepcopy(self.cages)
#             for row in range(9):
#                 row_cages = list(filter(lambda cage: any(cell.row == row for cell in cage.cells), self.cages))
#                 all_in_row = list(filter(lambda cage: all(cell.row == row for cell in cage.cells), row_cages))
#                 not_all_in_row = list(set(row_cages) - set(all_in_row))
#
#                 cells_falling_out = []
#                 cells_just_staying_in = []
#                 for cage in not_all_in_row:
#                     for cell in cage.cells:
#                         if cell.row != row:
#                             cells_falling_out.append(cell)
#                         else:
#                             cells_just_staying_in.append(cell)
#                 if cells_just_staying_in:
#                     # if not(Cage(sum(cage.total for cage in row_cages)-45, cells_falling_out) in self.cages):
#                     #     temp_cages.append(Cage(sum(cage.total for cage in row_cages)-45, cells_falling_out))
#                     if not(45-sum(cage.total for cage in all_in_row) == 0):
#                         if not(Cage(45-sum(cage.total for cage in all_in_row), cells_just_staying_in) in self.cages):
#                             temp_cages.append(Cage(45-sum(cage.total for cage in all_in_row), cells_just_staying_in))
#                             change_made = True
#             self.cages = temp_cages
#             #break
#             # TODO ^ REmove this outer break
#             if change_made:
#                 continue
#
#             # Cages cover all but one on column
#
#             temp_cages = copy.deepcopy(self.cages)
#             for col in range(9):
#                 col_cages = list(filter(lambda cage: any(cell.col == col for cell in cage.cells), self.cages))
#                 all_in_col = list(filter(lambda cage: all(cell.col == col for cell in cage.cells), col_cages))
#                 not_all_in_col = list(set(col_cages) - set(all_in_col))
#
#                 cells_falling_out = set()
#                 cells_just_staying_in = set()
#                 for cage in not_all_in_col:
#                     for cell in cage.cells:
#                         if cell.col != col:
#                             cells_falling_out.add(cell)
#                         else:
#                             cells_just_staying_in.add(cell)
#
#                 if cells_just_staying_in:
#                     # if not(Cage(sum(cage.total for cage in col_cages)-45, cells_falling_out) in self.cages):
#                     #     temp_cages.append(Cage(sum(cage.total for cage in col_cages)-45, cells_falling_out))
#                     if not (45 - sum(cage.total for cage in all_in_col) == 0):
#                         if 45 - sum(cage.total for cage in all_in_col) == 40:
#                             print(cells_just_staying_in)
#                         if not (Cage(45 - sum(cage.total for cage in all_in_col), cells_just_staying_in) in self.cages):
#                             temp_cages.append(Cage(45 - sum(cage.total for cage in all_in_col), cells_just_staying_in))
#                             change_made = True
#             self.cages = temp_cages
#             # break
#             # TODO ^ REmove this outer break
#             if change_made:
#                 continue
#
#             print("\n" * 10, self.cages)
#             print(self)
#
#
#             # Cages cover all but one in box
#
#
#
#
#
#
#             # break