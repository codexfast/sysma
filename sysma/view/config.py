
from sqlalchemy.orm import Session
from tkinter import messagebox

from models.sys import GeneralSettings
from modules.syspl.models.syspl import SysplLogin
from modules.sysfazenda.models.sysfazenda import SysFazendalConfig
from view.base import BaseWindow, BaseForm
from config import DB_ENGINE

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

        # set vars

        self.user_sispl_var = customtkinter.StringVar(value=None)
        self.password_sispl_var = customtkinter.StringVar(value=None)
        self.key_sysfazenda_var = customtkinter.StringVar(value=None)
        self.headless_mode_var = customtkinter.StringVar(value="checked")

        self.load_config()
        self.add_widgets()

    def add_widgets(self):
        
        self.draw_title("Configurações")

        # Sispl area

        lb_sispl = customtkinter.CTkLabel(
			self,
            text="Sispl Login",
            font=customtkinter.CTkFont(family="Arial", size=15),
            text_color="#737373",
		)
        user_sispl = BaseForm.entry(self, 200, placeholder="Usuário", textvariable=self.user_sispl_var)
        password_sispl = BaseForm.entry(self, 200, placeholder="Senha", show="*", textvariable=self.password_sispl_var)

        ###

        # Sys Fazenda area
        lb_sysfazenda = customtkinter.CTkLabel(
			self,
            text="Anti Captcha",
            font=customtkinter.CTkFont(family="Arial", size=15),
            text_color="#737373",
		)

        key = BaseForm.entry(self, 410, placeholder="KEY", textvariable=self.key_sysfazenda_var, show="*")

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


        btn_save.place(x=355, y=380)

        # sispl place
        lb_sispl.place(x=40, y=88)
        user_sispl.place(x=40, y=113)
        password_sispl.place(x=250, y=113)

        ###

        # Sysfazenda place

        lb_sysfazenda.place(x=40, y=173)
        key.place(x=40, y=198)

        ###

        # Config options
        headless_check = customtkinter.CTkCheckBox(
            self, 
            text="Headless Mode", 
            onvalue="checked", 
            offvalue="notchecked", 
            variable=self.headless_mode_var
        )

        headless_check.place(x=40, y=271)

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
            config_sysfazenda:SysFazendalConfig = session.query(SysFazendalConfig).one_or_none()
            general:GeneralSettings = session.query(GeneralSettings).one_or_none()

            if login_syspl:
                self.user_sispl_var.set(login_syspl.username)
                self.password_sispl_var.set(login_syspl.password)

            if config_sysfazenda:
                self.key_sysfazenda_var.set(config_sysfazenda.anti_captcha_key)

            if general:
                self.headless_mode_var.set("checked" if general.headless_mode else "notchecked")

            else:
                session.add(GeneralSettings(headless_mode=True))
                session.commit()


    def set_config(self):

        with Session(DB_ENGINE) as session, session.begin():

            login_syspl:SysplLogin = session.query(SysplLogin).one_or_none()
            config_sysfazenda:SysFazendalConfig = session.query(SysFazendalConfig).one_or_none()
            config_sysfazenda:SysFazendalConfig = session.query(SysFazendalConfig).one_or_none()
            general:GeneralSettings = session.query(GeneralSettings).one_or_none()


            if config_sysfazenda:
                config_sysfazenda.anti_captcha_key = self.key_sysfazenda_var.get()

            else:
                # caso não exista dados para key, cria no banco
                session.add(SysFazendalConfig(anti_captcha_key=self.key_sysfazenda_var.get()))

            if login_syspl:
                login_syspl.username = self.user_sispl_var.get()
                login_syspl.password = self.password_sispl_var.get()

            else:
                # caso não exista dados para login, cria no banco
                session.add(SysplLogin(username=self.user_sispl_var.get(), password=self.password_sispl_var.get()))

            if general:
                general.headless_mode = True if self.headless_mode_var.get() == "checked" else False
            


        messagebox.showinfo("Sucesso!", "Todas suas configurações foram salvas", parent=self)
