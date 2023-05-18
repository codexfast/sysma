import customtkinter as CTK
import time
from controller.core.web import create_webdriver

class App(CTK.CTk):
    def __init__(self):
        super().__init__()

        self.bar = CTK.CTkProgressBar(master=self,
                                    orientation='horizontal',
                                    mode='determinate')
        
        self.bar.grid(row=10, column=0, pady=10, padx=20, sticky="n")
        

        car = 788
        iter_ = 1/car

        # Set default starting point to 0
        self.bar.set(0)
        
        self.bar.start()
        
        for c in range(1,car):
            self.update()
            time.sleep(.5)
            self.bar.set(c*(iter_))
            print(c*(iter_))

        self.bar.stop()


driver = create_webdriver()
