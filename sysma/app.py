import customtkinter
import config

from view import HomeScreen
from view.home.nav import Navbar


class App(customtkinter.CTk):
        
        def __init__(self):
            super().__init__()

            # config windows
            self.title('Sysma')
            # self.geometry('600x450')
            self.minsize(width=600, height=450)
            self.after(0, lambda:self.state('zoomed'))
            
            self.iconbitmap(default=config.Images.ICON)

            # set grid layout 1x2
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1) 
			
            # Stacked
            Navbar(self)
            HomeScreen(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()