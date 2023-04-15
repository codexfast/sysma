from view.base import BaseWindow


class NewProjectWindow(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center(400,150)

