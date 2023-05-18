"""
Read and write xlsx files
"""

import openpyxl
import datetime

from openpyxl.styles import PatternFill, Font
from openpyxl.styles.colors import Color

my_red = Color(rgb='00FF0000')
my_green = Color(rgb='0050C878')

def format_with_date(text: str) -> str:
    return datetime.datetime.now().strftime(f"%d-%m-%Y.%H-%M-%S.{text}")


class Xlsx:

    """
    xlsx_file is path to Excel file
    """

    def __init__(self, xlsx_file):
        self.xlsx_file = xlsx_file
        self.ss = openpyxl.load_workbook(filename=xlsx_file)
        self.ws = self.ss[self.ss.active.title]

