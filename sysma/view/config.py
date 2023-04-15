from view.base import BaseWindow


class Configs(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center(500,350)
        self.title("configurações")

