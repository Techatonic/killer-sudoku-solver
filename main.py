import concurrent
import os
import json

from more_itertools import grouper

from CSP import Sudoku
from sudokuViewer import view_sudoku


def run_file(filename):
    file_path = "./sudokus/" + filename
    with open(file_path, "r") as file:
        data = json.load(file)

    # killer_sudoku = KillerSudoku(data['grid'], data['cages'], data['filledGrid'])
    # has_generic_solution = killer_sudoku.solve()

    sudoku = Sudoku(data['grid'], data['cages'], data['filledGrid'])
    has_generic_solution = sudoku.solve()

    # TODO Uncomment this
    if not has_generic_solution:
        os.remove(file_path)
        print(f'Removed {file_path}')
    else:
        os.rename(file_path, "./confirmed_sudokus/" + filename)
        print(f'Kept {file_path}')


def run_through_directory(files):
    for file in files:
        filename = os.fsdecode(file)
        print(f'filename: {filename}')
        if filename.endswith(".json"):
            run_file(filename)
        else:
            continue
        # # TODO Remove this
        # break


if __name__ == '__main__':
    directory = os.fsencode("./sudokus/")
    files = os.listdir(directory)

    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(run_through_directory, group)
               for group in grouper(5, files)]
    concurrent.futures.wait(futures)
