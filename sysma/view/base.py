import customtkinter
import config

class BaseWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.callback)
        self.title("UwU")
        
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
    
    @staticmethod
    def open_top_level(parent, top_level, window):
        if top_level is None or not top_level.winfo_exists():
            top_level = window(parent)  # create window if its None or destroyed
            # self.toplevel_window.focus()
            top_level.attributes("-topmost", 1)
        else:
            top_level.focus()  # if window exists focus it