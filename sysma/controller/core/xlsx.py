"""
Read and write xlsx files
"""

import dataclasses
import openpyxl
import datetime
import typing
import abc

from openpyxl.styles import PatternFill, Font
from openpyxl.styles.colors import Color

my_red = Color(rgb='00FF0000')
my_green = Color(rgb='0050C878')

def format_with_date(text: str) -> str:
    return datetime.datetime.now().strftime(f"%d-%m-%Y.%H-%M-%S.{text}")

@dataclasses.dataclass
class Xlsx(abc.ABC):

    """
    xlsx_file is path to Excel file
    """

    xlsx_file: str
    book: openpyxl.Workbook = dataclasses.field(repr=False, default=None)
    sheet: openpyxl.Workbook = dataclasses.field(repr=False, default=None)

    def __post_init__(self):
        self.book = openpyxl.load_workbook(self.xlsx_file)

    def _read(self, sheet: typing.AnyStr) -> typing.Generator:
        self.sheet = self.book[sheet]

        return self.sheet.iter_rows()

    def _writefile(self, filename: typing.AnyStr, data: typing.List[typing.List])  -> typing.NoReturn:
        """Create columns on sheet"""
        
        page_title = 'results'

        book = openpyxl.Workbook()

        results_page = book["Sheet"]
        results_page.title = page_title

        for columns in data:
            results_page.append(columns)

            for c in columns:
                if '-1' == c:
                    for i in list(results_page.iter_rows())[-1]:
                        i.fill = PatternFill(patternType='solid', fgColor=my_red)
                        i.font = Font(color="FFFFFFFF")

                elif 'COM' == c:
                    for i in list(results_page.iter_rows())[-1]:
                        i.fill = PatternFill(patternType='solid', fgColor=my_green)
                        i.font = Font(color="FFFFFFFF")

        book.save(filename)
        book.close()

