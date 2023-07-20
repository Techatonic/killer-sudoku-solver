import tkinter as tk

def create_killer_sudoku_gui(root, puzzle_data):
    def create_sudoku_grid(frame):
        # Create a 9x9 Sudoku grid with entry widgets
        for i in range(9):
            for j in range(9):
                cell_value = puzzle_data['grid'][i][j]
                entry = tk.Entry(frame, width=2, font=("Arial", 20), justify='center')
                if cell_value != 0:
                    entry.insert(0, str(cell_value))
                entry.grid(row=i, column=j)

    def create_killer_cages(frame):
        # Draw cages and their sums on the Sudoku grid
        for cage in puzzle_data['cages']:
            cage_cells = cage['cells']
            cage_sum = cage['sum']
            for cell in cage_cells:
                row, col = cell
                frame.grid_slaves(row=row, column=col)[0].config(bg='lightblue')
            label = tk.Label(frame, text=str(cage_sum), font=("Arial", 12, "bold"))
            label.grid(row=cage_cells[0][0], column=cage_cells[0][1])

    sudoku_frame = tk.Frame(root)
    sudoku_frame.pack()

    create_sudoku_grid(sudoku_frame)
    create_killer_cages(sudoku_frame)


def show_sudoku(sudoku):
    root = tk.Tk()
    root.title("Killer Sudoku GUI")

    # Load the JSON data and pass it to the GUI function
    create_killer_sudoku_gui(root, sudoku)

    root.mainloop()