import os
import random

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from animal_quotes import animal_quotes, animal_names

font_name = 'garamond'
font_path = 'garamond.ttf'


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

        # Add blue border
        style = getSampleStyleSheet()["Normal"]

        # Create a custom ParagraphStyle
        animal_quote_style = ParagraphStyle(name='Normal_CENTER',
                                            parent=style,
                                            fontName=font_name,
                                            wordWrap='LTR',
                                            alignment=TA_CENTER,
                                            fontSize=12,
                                            leading=13,
                                            textColor=colors.black,
                                            borderPadding=0,
                                            leftIndent=0,
                                            rightIndent=0,
                                            spaceAfter=0,
                                            spaceBefore=0,
                                            splitLongWords=True,
                                            spaceShrinkage=0.05,
                                            )

        # show animal quote
        animal = random.choice(list(animal_quotes.keys()))
        animal_quote_text = animal_names[animal] + ': "' + random.choice(animal_quotes[animal]) + '"'
        para_text = Paragraph(animal_quote_text, style=animal_quote_style)
        para_text.wrapOn(c, 200, 200)

        # animal_quote_width = c.stringWidth(animal_quote_text, "Helvetica", 12)
        animal_quote_width = para_text.width
        animal_quote_x = (page_width - animal_quote_width) / 2
        animal_quote_y = 60
        c.setFont(font_name, 12)

        # wrap_string(c, animal_quote_text, animal_quote_x, animal_quote_y, 400)
        para_text.drawOn(c, animal_quote_x, animal_quote_y)
        # c.drawString(animal_quote_x, animal_quote_y, animal_quote_text)

        c.showPage()

    c.save()


def generate_pdf():
    # Create custom pdf font
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # Show all sudokus in folder
    directory = os.fsencode("./sudoku_imgs/")
    files = os.listdir(directory)
    directory_path = "./sudoku_imgs/"
    add_images_to_pdf([directory_path + os.fsdecode(file) for file in files], 'test.pdf')


generate_pdf()
