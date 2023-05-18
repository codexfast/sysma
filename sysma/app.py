import customtkinter
import config

from view import HomeScreen
from view.home.nav import Navbar

# from model.automobiles import Automobiles
# from sqlalchemy import select
# from sqlalchemy.orm import Session

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


        # I'm trying how add into database
        # with Session(config.DB_ENGINE) as session:
            # session.add(Automobiles(placa="ASDASD", renavam="07078708", chassi="ASAD123SFA3"))
            # session.commit()
            # res = session.query(Automobiles).all()

            # print("Res is ",res)

if __name__ == "__main__":
    app = App()
    app.mainloop()