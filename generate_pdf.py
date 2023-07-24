import os

from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas


def add_images_to_pdf(image_paths, output_filename):
    c = canvas.Canvas(output_filename, pagesize=A5)

    page_width, page_height = A5
    image_width, image_height = 325, 325

    center_x = (page_width - image_width) / 2
    center_y = (page_height - image_height) / 2

    for index, image_path in enumerate(image_paths, start=1):
        # show sudoku
        c.drawImage(image_path, center_x, center_y, width=image_width, height=image_height)

        # show text
        sudoku_number_text = f'Sudoku #{index}'
        sudoku_number_width = c.stringWidth(sudoku_number_text, "Helvetica", 12)
        sudoku_number_x = (page_width - sudoku_number_width) / 2
        sudoku_number_y = page_height - 90
        c.setFont('Helvetica', 12)
        c.drawString(sudoku_number_x, sudoku_number_y, sudoku_number_text)

        c.showPage()

    c.save()


def generate_pdf():
    # Show all sudokus in folder
    directory = os.fsencode("./sudoku_imgs/")
    files = os.listdir(directory)
    directory_path = "./sudoku_imgs/"
    add_images_to_pdf([directory_path + os.fsdecode(file) for file in files], 'test.pdf')

generate_pdf()
