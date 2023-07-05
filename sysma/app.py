import customtkinter
import config

from view import HomeScreen
from view.home.nav import Navbar


class App(customtkinter.CTk):
        
    def __init__(self):
        super().__init__()

        # config windows
        self.title('Sysma')

        width = 740
        height = 450

        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        # self.minsize(width=600, height=450)
        # self.after(0, lambda:self.state('zoomed'))
   
        self.iconbitmap(default=config.Images.ICONV2)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) 
        
        # Stacked
        Navbar(self)
        HomeScreen(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()