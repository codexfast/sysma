import customtkinter
import config

class BaseWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self._destroy)

        self.title("UwU")
        
        self.master = master
        self.master.withdraw()

        self.DEFAULT_OPEN_XLSX = {
            "parent":self,
            "initialdir":config.DOCUMENTS_FOLDER,
            "title":"Selecione uma planilha",
            "filetypes":(
                ("Arquivo Excel", "*.xlsx*"),
            ),
        }

        self.DEFAULT_SELECT_FOLDER = {
            "parent":self,
            "initialdir":config.DOCUMENTS_FOLDER,
            "title":"Selecione uma pasta",
        }

    def draw_title(self, title: str):
        title_label = customtkinter.CTkLabel(
            self, 
            text=title,
            font=customtkinter.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#4A4A4A"

        )
        title_label.place(x=40, y=40)
        
    def _destroy(self):

        self.master.state("normal")
        self.destroy()
        self.master.deiconify()

    def center(self, width, height):

        screen_width = self.master.winfo_screenwidth()  # Width of the screen
        screen_height = self.master.winfo_screenheight() # Height of the screen
        
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry("%dx%d+%d+%d" % (
            width,
            height,
            x,
            y
        ))
    
    @staticmethod
    def open_top_level(parent, top_level, window, **kwargs):
        if top_level is None or not top_level.winfo_exists():
            top_level = window(parent, **kwargs)  # create window if its None or destroyed
            # self.toplevel_window.focus()
            top_level.attributes("-topmost", 1)
        else:
            top_level.focus()  # if window exists focus it

class BaseForm:
    _CONFIG = {
        "fg_color":"#E7EFEE",
        "border_width": 0,
        "placeholder_text_color":"#9E9E9E"
    }

    @staticmethod
    def entry(parent, width: int, height: int = 40, placeholder: str = "Entry", **kwargs) -> customtkinter.CTkEntry:
        return customtkinter.CTkEntry(
            parent, 
            width=width, 
            height=height, 
            placeholder_text=placeholder,
            **BaseForm._CONFIG,
            **kwargs
        )

    @staticmethod
    def button(parent, text: str, command=None):
        return customtkinter.CTkButton(
            parent,
            text=text,
            font=customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            fg_color="#3B97D3",
            width=105,
            height=40,
            corner_radius=20,
            text_color="#fff",
            command=command
        )
    
    @staticmethod
    def buttonv2(parent, width: int, height: int, image, textvariable=None, command=None, **kwargs):
        return customtkinter.CTkButton(
            parent,
            font=customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            fg_color="#E7EFEE",
            image=image,
            width=width,
            height=height,
            corner_radius=8,
            text_color="#9E9E9E",
            command=command,
            compound="right",
            border_spacing=0,
            border_width=0,
            anchor="w",
            textvariable=textvariable,
            hover_color="#CED7D6",
            **kwargs
        )
    
    @staticmethod
    def buttonv3(parent, width: int, height: int, **kwargs):
        """For images"""

        return customtkinter.CTkButton(
            parent,
            text=None,
            width=width,
            height=height,
            hover=None,
            fg_color="transparent",
            bg_color="transparent",
            
            **kwargs
        )

    @staticmethod
    def textbox(parent):
        return customtkinter.CTkTextbox(
            parent,
            fg_color=BaseForm._CONFIG['fg_color'],
            border_width=BaseForm._CONFIG['border_width']
        )
