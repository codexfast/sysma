from view.base import BaseWindow

class ImportAssets(BaseWindow):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center(400,400)
        self.draw_title("Importação de placas/renavam")

