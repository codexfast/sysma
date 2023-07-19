
from sqlalchemy.orm import Session
from tkinter import messagebox

from models.sys import GeneralSettings
from modules.syspl.models.syspl import SysplLogin, SysplConfig
from modules.sysfazenda.models.sysfazenda import SysFazendalConfig
from view.base import BaseWindow, BaseForm
from config import DB_ENGINE

from controllers.core.recaptcha import ReCaptcha

import customtkinter


class Configs(BaseWindow):

    # 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center(500,464)
        self.configure(fg_color=("#fff", "#333"))
        self.resizable(False, False)
        # self.iconbitmap()
        self.title("configurações")

        # set vars

        self.user_sispl_var = customtkinter.StringVar(value=None)
        self.password_sispl_var = customtkinter.StringVar(value=None)
        self.balance_var = customtkinter.StringVar()
        self.key_sysfazenda_var = customtkinter.StringVar(value=None)
        self.headless_mode_var = customtkinter.StringVar(value="checked")
        self.xtime_var = customtkinter.StringVar(value=5)

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

        lb_balance = customtkinter.CTkLabel(
			self,
            text="Saldo",
            font=customtkinter.CTkFont(family="Arial", size=15),
            text_color="#737373",
            
		)

        lb_xtime = customtkinter.CTkLabel(
			self,
            text="Sispl X Time",
            font=customtkinter.CTkFont(family="Arial", size=15),
            text_color="#737373",
            
		)

        xtime = BaseForm.entry(self, 271, placeholder="XTIME", textvariable=self.xtime_var)

        key = BaseForm.entry(self, 271, placeholder="KEY", textvariable=self.key_sysfazenda_var, show="*")

        balance = BaseForm.entry(self, 128, placeholder="Saldo: $0,00", textvariable=self.balance_var, state="disable")

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
        
        # sispl x time
        lb_xtime.place(x=40, y=173)
        xtime.place(x=40, y=198)
        ###

        # Sysfazenda place

        lb_sysfazenda.place(x=40, y=258)
        lb_balance.place(x=322, y=258)
        key.place(x=40, y=283)
        balance.place(x=322, y=283)

        ###

        # Config options
        headless_check = customtkinter.CTkCheckBox(
            self, 
            text="Headless Mode", 
            onvalue="checked", 
            offvalue="notchecked", 
            variable=self.headless_mode_var
        )

        headless_check.place(x=40, y=343)

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
            syspl_config:SysplConfig = session.query(SysplConfig).one_or_none()

            if login_syspl:
                self.user_sispl_var.set(login_syspl.username)
                self.password_sispl_var.set(login_syspl.password)

            if config_sysfazenda:
                self.key_sysfazenda_var.set(config_sysfazenda.anti_captcha_key)

                balance = ReCaptcha.get_balance(config_sysfazenda.anti_captcha_key)

                self.balance_var.set(f"$ {balance}")

            if syspl_config:
                self.xtime_var.set(syspl_config.xtime)

            if general:
                self.headless_mode_var.set("checked" if general.headless_mode else "notchecked")

            else:
                session.add(GeneralSettings(headless_mode=True))
                session.commit()


    def set_config(self):
        
        try:
            xtime = int(self.xtime_var.get())
        except ValueError:
            messagebox.showerror("Atenção!", "Xtime deve ser um valor inteiro/flutuante", parent=self)


            return 0

        with Session(DB_ENGINE) as session, session.begin():

            login_syspl:SysplLogin = session.query(SysplLogin).one_or_none()
            config_sysfazenda:SysFazendalConfig = session.query(SysFazendalConfig).one_or_none()
            config_sysfazenda:SysFazendalConfig = session.query(SysFazendalConfig).one_or_none()
            general:GeneralSettings = session.query(GeneralSettings).one_or_none()
            syspl_config:SysplConfig = session.query(SysplConfig).one_or_none()



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

            if syspl_config:
                syspl_config.xtime = xtime

            else:
                session.add(SysplConfig(xtime=xtime))

            if general:
                general.headless_mode = True if self.headless_mode_var.get() == "checked" else False
            


        messagebox.showinfo("Sucesso!", "Todas suas configurações foram salvas", parent=self)
