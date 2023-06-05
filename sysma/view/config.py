
from sqlalchemy.orm import Session
from tkinter import messagebox

from modules.syspl.models.syspl import SysplLogin
from view.base import BaseWindow, BaseForm
from config import DB_ENGINE

import customtkinter


class Configs(BaseWindow):

    # 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center(500,245)
        self.configure(fg_color=("#fff", "#333"))
        self.resizable(False, False)
        # self.iconbitmap()
        self.title("configurações")

        # set vars

        self.user_sispl_var = customtkinter.StringVar(value="")
        self.password_sispl_var = customtkinter.StringVar(value="")

        self.load_config()
        self.add_widgets()

    def add_widgets(self):
        
        self.draw_title("Configurações")

        # Sispl area

        lb_sispl = customtkinter.CTkLabel(
			self,
            text="Sispl login",
            font=customtkinter.CTkFont(family="Arial", size=15),
            text_color="#737373",
		)
        user_sispl = BaseForm.entry(self, 200, placeholder="Usuário", textvariable=self.user_sispl_var)
        password_sispl = BaseForm.entry(self, 200, placeholder="Senha", show="*", textvariable=self.password_sispl_var)

        ###

        btn_save = customtkinter.CTkButton(
            self,
            text="Salvar",
            font=customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            fg_color="#3B97D3",
            width=105,
            height=30,
            corner_radius=15,
            command=self.set_config
        )

        btn_save.place(x=355, y=175)

        # sispl place
        lb_sispl.place(x=40, y=88)
        user_sispl.place(x=40, y=113)
        password_sispl.place(x=250, y=113)

        ###

        # Config options
		# ... nothing here
        
        # lb_no_config = customtkinter.CTkLabel(
		# 	self,
        #     text="Nenhuma configuração\ndisponivel no momento",
        #     font=customtkinter.CTkFont(family="Arial", size=20, weight="bold"),
        #     text_color="#A6A6A6",
		# )

        # lb_no_config.place(x=118, y=199)
        # lb_no_config.place(relx=0.5, rely=0.5, anchor="center")

    def load_config(self):

        with Session(DB_ENGINE) as session:

            login_syspl:SysplLogin = session.query(SysplLogin).one_or_none()

            if login_syspl:
                self.user_sispl_var.set(login_syspl.username)
                self.password_sispl_var.set(login_syspl.password)


    def set_config(self):

        with Session(DB_ENGINE) as session, session.begin():

            # sispl login
            login_syspl:SysplLogin = session.query(SysplLogin).one_or_none()

            if login_syspl:
                login_syspl.username = self.user_sispl_var.get()
                login_syspl.password = self.password_sispl_var.get()

            else:
                # caso não exista dados para login, cria no banco
                session.add(SysplLogin(username=self.user_sispl_var.get(), password=self.password_sispl_var.get()))


        messagebox.showinfo("Sucesso!", "Todas suas configurações foram salvas", parent=self)
