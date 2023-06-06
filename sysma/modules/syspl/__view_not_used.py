from view.base import BaseWindow
from .screen.worker import Worker
from .screen.history import History

from sqlalchemy.orm import Session
from models.automobiles import Automobiles
from .models.syspl import SysplLogin
from controllers.functionalities.import_export_xlsx import do_import

import config
import customtkinter
import typing

from tkinter import messagebox, StringVar

class View(BaseWindow):

    def __init__(self,  master, project_id: int, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.toplevel_window = None
        self.project_id = project_id


        self.center(700, 450)
        self.title("Syspl")
        self.draw_title("Syspl")
        self.configure(fg_color=("#fff", "#333"))
        self.resizable(False, False)

        self.add_widgets()


    def _destroy(self):
        return super()._destroy()

    def get_login(self) -> typing.Tuple[str, str]:

        # Renan login
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
            width=87,
            height=87,
            text=None,
            fg_color="transparent",
            corner_radius=0,
            command=lambda: BaseWindow.open_top_level(self, self.toplevel_window, History),
            image=config.Images.FOLDERCHECKV2
            # state="disabled"
        )

        btn_upload_file = customtkinter.CTkButton(
            self,
            width=87,
            height=87,
            text=None,
            fg_color="transparent",
            corner_radius=0,
            command=lambda: do_import(self, self.project_id),
            image=config.Images.UPLOADFILE
            # state="disabled"
        )



        # lb_.place(x=308, y=140)

        btn_start.place(x=298, y=280)
        btn_completed.place(x=377, y=130)
        btn_upload_file.place(x=235, y=130)

    def open_worker(self, user_var, pass_var):


        user_var.set("36490625857")
        pass_var.set("rennan10")
        
        if user_var.get() and pass_var.get():

            with Session(config.DB_ENGINE) as session:

                count = session.query(Automobiles).count()
                login = session.query(SysplLogin).one_or_none()

                if login:
                    login.username = user_var.get()
                    login.password = pass_var.get()

                    session.commit()

                if count:
                    BaseWindow.open_top_level(self, self.toplevel_window, Worker, project_id=self.project_id)
                
                else:
                    messagebox.showwarning("0", "Sem dados para processar!", parent=self)

        else:

            messagebox.showwarning("0", "Usuário ou senha está vazio.", parent=self)

