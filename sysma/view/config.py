from view.base import BaseWindow
import customtkinter

class Configs(BaseWindow):

    # 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center(500,450)
        self.configure(fg_color=("#fff", "#333"))
        self.resizable(False, False)
        # self.iconbitmap()
        self.title("configurações")

        self.add_widgets()

    def add_widgets(self):
        
        self.draw_title("Configurações")

        btn_save = customtkinter.CTkButton(
            self,
            text="Salvar",
            font=customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            fg_color="#3B97D3",
            width=105,
            height=30,
            corner_radius=15,
            # state="disabled"
        )

        # btn_save.place(x=355, y=380)

        # Config options
		# ... nothing here
        
        lb_no_config = customtkinter.CTkLabel(
			self,
            text="Nenhuma configuração\ndisponivel no momento",
            font=customtkinter.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#A6A6A6",
		)

        # lb_no_config.place(x=118, y=199)
        lb_no_config.place(relx=0.5, rely=0.5, anchor="center")
