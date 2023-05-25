from view.base import BaseWindow
from .screen.worker import Worker
from .screen.history import History

from sqlalchemy.orm import Session
from models.automobiles import Automobiles
from .models.syspl import SysplLogin

import config
import customtkinter
import typing

from tkinter import messagebox, StringVar

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

    def get_login(self) -> typing.Tuple[str, str]:

        username = ""
        password = ""
        
        with Session(config.DB_ENGINE) as session:
            login = session.query(SysplLogin).one_or_none()

            if login:
                username = login.username
                password = login.password

            else:

                session.add(SysplLogin(username="", password=""))
                session.commit()

        return (username, password)
    

    def add_widgets(self):

        _u, _p = self.get_login()

        username_var = StringVar(value=_u)
        password_var = StringVar(value=_p)

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
            **entry_config,
            textvariable=username_var,

        )

        password = customtkinter.CTkEntry(
            self, 
            width=220, 
            height=40, 
            placeholder_text="Senha",
            textvariable=password_var,
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
            command=lambda: self.open_worker(username_var, password_var)
            # state="disabled"
        )

        btn_completed = customtkinter.CTkButton(
            self,
            width=21,
            height=21,
            text=None,
            fg_color="transparent",
            corner_radius=0,
            command=lambda: BaseWindow.open_top_level(self, self.toplevel_window, History),
            image=config.Images.FOLDERCHECK
            # state="disabled"
        )



        lb_.place(x=308, y=140)
        username.place(x=240, y=174)
        password.place(x=240, y=223)
        btn_start.place(x=298, y=280)
        btn_completed.place(x=648, y=41)

    def open_worker(self, user_var, pass_var):

        if user_var.get() and pass_var.get():

            with Session(config.DB_ENGINE) as session:

                count = session.query(Automobiles).count()
                login = session.query(SysplLogin).one_or_none()

                if login:
                    login.username = user_var.get()
                    login.password = pass_var.get()

                    session.commit()

                if count:
                    BaseWindow.open_top_level(self, self.toplevel_window, Worker)
                
                else:
                    messagebox.showwarning("0", "Sem dados para processar!", parent=self)

        else:

            messagebox.showwarning("0", "Usuário ou senha está vazio.", parent=self)

