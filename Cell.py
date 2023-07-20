class Cell:

    def __init__(self, row, col, val=None):
        self.row = row
        self.col = col
        self.val = val

    def __str__(self):
        return f'({self.row}, {self.col})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col  # and self.val == other.val

    def __hash__(self):
        return hash((self.row, self.col))
