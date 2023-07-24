import io
import json
import os
import time
import tkinter as tk

import pyautogui as pyautogui
from PIL import Image, ImageGrab
import mss.tools

from CSP import Sudoku
from pyscreenshot import grab


def create_killer_sudoku_gui(root, sudoku, filename):
    def create_sudoku_grid(frame):
        # Create a 9x9 Sudoku grid with entry widgets
        for x in range(10):
            width = 0.5
            if x == 0:
                width = 6
            elif x % 3 == 0:
                width = 1.5
            canvas.create_line((x * cell_size, 0), (x * cell_size, 9 * cell_size), fill='black', width=width)
        for y in range(10):
            width = 0.5
            if y == 0:
                width = 6
            elif y % 3 == 0:
                width = 1.5
            canvas.create_line((0, y * cell_size), (9 * cell_size, y * cell_size), fill='black', width=width)

        for i in range(9):
            for j in range(9):
                cell_value = sudoku.board[i][j].val
                if cell_value != 0:
                    canvas.create_text(i * cell_size + cell_size / 2, j * cell_size + cell_size / 2,
                                       text=cell_value, font=("Arial", 12, "bold"))
                # entry = tk.Entry(frame, width=2, font=("Arial", 20), justify='center')
                # if cell_value != 0:
                #     entry.insert(0, str(cell_value))
                # entry.grid(row=i, column=j)

    def draw_killer_cages(frame):
        # Draw cages and their sums on the Sudoku grid
        for cage in sudoku.cages:
            cage_cells = cage.cells
            cage_sum = cage.total

            # Display the sum in the top-left corner of the cage
            first_cage_cell = min(cage_cells, key=lambda cell: (cell.row, cell.col))
            cage_sum_object = canvas.create_text(first_cage_cell.col * cell_size + cell_size / 5,
                                                 first_cage_cell.row * cell_size + cell_size / 5,
                                                 text=str(cage_sum), font=("Arial", 9, "bold"))

            # Draw dashed lines for the cage
            cage_offset = 5

            cells = sorted(cage.cells, key=lambda cell: (cell.row, cell.col))
            for index, cell in enumerate(cells):
                # Right line
                if not (any(other.row == cell.row and other.col == cell.col + 1 for other in cells)):
                    xPos = (cell.col + 1) * cell_size - cage_offset
                    startY = None
                    if any(other.row == cell.row - 1 and other.col == cell.col for other in cells):
                        startY = cell.row * cell_size
                    else:
                        startY = cell.row * cell_size + cage_offset
                    stopY = None
                    if any(other.row == cell.row + 1 and other.col == cell.col for other in cells):
                        stopY = (cell.row + 1) * cell_size
                    else:
                        stopY = (cell.row + 1) * cell_size - cage_offset

                    canvas.create_line((xPos, startY), (xPos, stopY), dash=(2, 2), fill='black')

                # Bottom line
                if not (any(other.row == cell.row + 1 and other.col == cell.col for other in cells)):
                    yPos = (cell.row + 1) * cell_size - cage_offset
                    startX = None
                    if any(other.row == cell.row and other.col == cell.col - 1 for other in cells):
                        startX = cell.col * cell_size
                    else:
                        startX = cell.col * cell_size + cage_offset
                    stopX = None
                    if any(other.row == cell.row and other.col == cell.col + 1 for other in cells):
                        stopX = (cell.col + 1) * cell_size
                    else:
                        stopX = (cell.col + 1) * cell_size - cage_offset

                    canvas.create_line((startX, yPos), (stopX, yPos), dash=(2, 2), fill='black')

                # Top line
                if not (any(other.row == cell.row - 1 and other.col == cell.col for other in cells)):
                    yPos = cell.row * cell_size + cage_offset
                    startX = None
                    # if index == 0:
                    # if False:
                    #    cage_sum_text_dimensions = canvas.bbox(cage_sum_object)
                    #    startX = cell.col * cell_size + (cage_sum_text_dimensions[2] - cage_sum_text_dimensions[0])
                    # else:
                    if any(other.row == cell.row and other.col == cell.col - 1 for other in cells):
                        startX = cell.col * cell_size
                    else:
                        startX = cell.col * cell_size + cage_offset
                    stopX = None
                    if any(other.row == cell.row and other.col == cell.col + 1 for other in cells):
                        stopX = (cell.col + 1) * cell_size
                    else:
                        stopX = (cell.col + 1) * cell_size - cage_offset

                    canvas.create_line((startX, yPos), (stopX, yPos), dash=(2, 2), fill='black')

                # Left line
                if not (any(other.row == cell.row and other.col == cell.col - 1 for other in cells)):
                    xPos = cell.col * cell_size + cage_offset
                    startY = None
                    if any(other.row == cell.row - 1 and other.col == cell.col for other in cells):
                        startY = cell.row * cell_size
                    else:
                        startY = cell.row * cell_size + cage_offset
                    stopY = None
                    if any(other.row == cell.row + 1 and other.col == cell.col for other in cells):
                        stopY = (cell.row + 1) * cell_size
                    else:
                        stopY = (cell.row + 1) * cell_size - cage_offset

                    canvas.create_line((xPos, startY), (xPos, stopY), dash=(2, 2), fill='black')

    cell_size = 80  # Adjust this value to change the cell size
    canvas_width = cell_size * 9
    canvas_height = cell_size * 9

    sudoku_frame = tk.Frame(root)
    sudoku_frame.pack()

    canvas = tk.Canvas(sudoku_frame, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()
    # canvas.pack(padx=(10, 10), pady=(10, 10))

    create_sudoku_grid(canvas)
    draw_killer_cages(canvas)
    return canvas


def take_screenshot(filename, canvas):
    # save window as image
    directory = './sudoku_imgs/'
    filename = directory + filename

    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"] + 0,  # 100px from the top
            "left": mon["left"] + 479,  # 100px from the left
            "width": 722,
            "height": 722,
            "mon": monitor_number,
        }

        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output=filename + '.png')

    # x, y = canvas.winfo_rootx(), canvas.winfo_rooty()
    # w, h = canvas.winfo_width(), canvas.winfo_height()
    # pyautogui.screenshot(filename+'.png', region=(x, y, w, h))




def show_sudoku(sudoku, filename):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Killer Sudoku GUI")

    # Load the JSON data and pass it to the GUI function
    canvas = create_killer_sudoku_gui(root, sudoku, filename)

    root.update()
    if not os.path.exists(filename + '.png'):
        root.after(1000, take_screenshot, filename, canvas)
        root.after(2000, root.destroy)

    root.mainloop()


def view_sudokus():
    # Show all sudokus in folder
    directory = os.fsencode("./confirmed_sudokus/")
    files = os.listdir(directory)
    for i, _file in enumerate(files):
        filename = os.fsdecode(_file)
        print(f'filename: {filename}')

        file_path = "./confirmed_sudokus/" + filename
        with open(file_path, "r") as file:
            data = json.load(file)

        sudoku = Sudoku(data['grid'], data['cages'], data['filledGrid'])

        show_sudoku(sudoku, filename.rstrip('.json'))
        # if i == 1:
        #     break


view_sudokus()
