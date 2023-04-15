import customtkinter

class BaseWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.callback)
        
        self.master = master
        self.master.withdraw()

    def callback(self):

        self.master.state("normal")
        self.destroy()
        self.master.deiconify()

    def center(self, width, height):
        self.geometry("%dx%d+%d+%d" % (
            width,
            height,
            self.master.winfo_x() + self.master.winfo_width() /4,
            self.master.winfo_y() + self.master.winfo_height()/4
        ))