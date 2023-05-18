from view.base import BaseWindow
from tkinter import ttk

class ProgressBar(BaseWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.center(400, 100)

        self.resizable(False, False)

        pb = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=200)
        pb.start()
        pb.pack()
