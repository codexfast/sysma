from view.base import BaseWindow
from .screen.worker import Worker
import config

import customtkinter

class View(BaseWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.toplevel_window = None


        self.center(700, 450)
        self.title("Syspl")
        self.draw_title("Syspl")
        self.configure(fg_color=("#fff", "#333"))
        self.resizable(False, False)

        self.add_widgets()

    def _destroy(self):
        return super()._destroy()
    
    def add_widgets(self):

        entry_config = {
            "fg_color":"#E7EFEE",
            "border_width": 0,
            "placeholder_text_color":"#9E9E9E"
        }

        lb_ = customtkinter.CTkLabel(
			self,
            text="Dados Login",
            font=customtkinter.CTkFont(family="Arial", size=15),
            text_color="#4A4A4A",
		)

        username = customtkinter.CTkEntry(
            self, 
            width=220, 
            height=40, 
            placeholder_text="Usuário",
            **entry_config
            
        )

        password = customtkinter.CTkEntry(
            self, 
            width=220, 
            height=40, 
            placeholder_text="Senha",
            show="*",
            **entry_config
        )

        btn_start = customtkinter.CTkButton(
            self,
            text="iniciar",
            font=customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            fg_color="#3B97D3",
            width=105,
            height=30,
            corner_radius=15,
            text_color="#fff",
            command=lambda: BaseWindow.open_top_level(self, self.toplevel_window, Worker)
            # state="disabled"
        )

        btn_completed = customtkinter.CTkButton(
            self,
            width=21,
            height=21,
            text=None,
            fg_color="transparent",
            corner_radius=0,
            command=lambda: BaseWindow.open_top_level(self, self.toplevel_window, Worker),
            image=config.Images.FOLDERCHECK
            # state="disabled"
        )



        lb_.place(x=308, y=140)
        username.place(x=240, y=174)
        password.place(x=240, y=223)
        btn_start.place(x=298, y=280)
        btn_completed.place(x=648, y=41)

