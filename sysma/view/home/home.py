
from controller.core.sysmas_resource import LoadSysmaResource
from view.projects.project import NewProjectWindow
from view.config import Configs as ConfigWindow
from view.base import BaseWindow
from tkinter import messagebox

# Modules viwers
from modules.syspl.view import View as SysplView

import customtkinter
import config



class HomeScreen:
    def __init__(self, parent) -> None:

        self.master = parent

        self.button_pad = {
            "padx":10,
            "pady":10
        }

        self.screen = customtkinter.CTkFrame(parent, corner_radius=0,fg_color=("#EDEDED", "gray25"))
        self.screen.grid(row=0, column=1, sticky="nsew")

        self.toplevel_window = None

        self.add_widgets()

        # calls 'create new project' function after splash screen is drawn
        # self.create_new_project()
        
        # calls 'Syspl' function after splash screen is drawn
        BaseWindow.open_top_level(
            self.master, 
            self.toplevel_window, 
            SysplView
        )

    def add_widgets(self):
        sub_frame = customtkinter.CTkFrame(
            self.screen, 
            width=375, 
            height=400,
            fg_color=("#D9D9D9","grey10"),
        )

        sub_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        new_project_btn = customtkinter.CTkButton(
            sub_frame, 
            text=None, 
            image=config.Images.NEW_PROJECT,
            fg_color="transparent",
            bg_color="transparent",
            # hover=None,
            hover_color="gray70",
            width=96,
            height=99,
            command=self.create_new_project,
            corner_radius=0,
            state="disabled"

        )

        projects_btn = customtkinter.CTkButton(
            sub_frame, 
            text=None, 
            image=config.Images.PROJECTS,
            fg_color="transparent",
            bg_color="transparent",
            # hover=None,
            hover_color="gray70",
            width=96,
            height=99,
            corner_radius=0,
            state="disabled"
        )

        dashboard_btn = customtkinter.CTkButton(
            sub_frame, 
            text=None, 
            image=config.Images.DASHBOARD,
            fg_color="transparent",
            bg_color="transparent",
            # hover=None,
            hover_color="gray70",
            width=96,
            height=99,
            corner_radius=0,
            state="disabled"
        )

        config_btn = customtkinter.CTkButton(
            sub_frame, 
            text=None, 
            image=config.Images.CONFIG,
            fg_color="transparent",
            bg_color="transparent",
            # hover=None,
            hover_color="gray70",
            width=96,
            height=99,
            corner_radius=0,
            command=self.change_configs
        )
        
        import_assets = customtkinter.CTkButton(
            sub_frame, 
            text=None, 
            image=config.Images.IMPORT_RESOURCE,
            fg_color="transparent",
            bg_color="transparent",
            # hover=None,
            hover_color="gray70",
            width=96,
            height=99,
            corner_radius=0,
            command=self.do_import
        )

        syspl = customtkinter.CTkButton(
            sub_frame, 
            text=None, 
            image=config.Images.SYSPL,
            fg_color="transparent",
            bg_color="transparent",
            # hover=None,
            hover_color="gray70",
            width=96,
            height=99,
            corner_radius=0,
            command=lambda: \
                BaseWindow.open_top_level(
                    self.master, 
                    self.toplevel_window, 
                    SysplView
            )
        )

        import_assets.grid(**self.button_pad, row=0, column=0)
        syspl.grid(**self.button_pad, row=0, column=1)
        config_btn.grid(**self.button_pad, row=0, column=2)

    def do_import(self):

        filename = customtkinter.filedialog.askopenfilename(
            initialdir=config.DOCUMENTS_FOLDER,
            title="Selecione uma planilha",
            filetypes=(
                ("Arquivo Excel", "*.xlsx*"),
            )
        )

        if filename:
            loaded_assets = LoadSysmaResource(filename)

            if loaded_assets.invalid_resources:
                report = messagebox.askyesno("Erro na planilha encontrado", "Deseja gerar planilha com os erros?", icon="warning")

                # if report: faça nova planilha de erros dos itens

            if loaded_assets.valid_resources:
                
                # caso a lista de placas/renavam/chassi seja carregada corretamente faça:
                if loaded_assets.count_resources > 0:
                    merge = messagebox.askyesnocancel("Mesclagem", "Dejesa mesclar aos veículos atuais?")

                    # Se nulo não faz nada
                    if not merge is None:

                        # aqui se True faz merge dos recursos
                        if merge:
                            loaded_assets.merge_resources()
                        else:
                            loaded_assets.record_resources()

                else:
                    loaded_assets.record_resources()

                messagebox.showinfo("Sucesso", "Dados importados com sucesso!")

            else:
                messagebox.showerror("Erro", "Dados não importados!")

            # BaseWindow.open_top_level(self.master, self.toplevel_window, ProgressBar)


    def create_new_project(self):
        BaseWindow.open_top_level(self.master, self.toplevel_window, NewProjectWindow)

    def change_configs(self):
        BaseWindow.open_top_level(self.master, self.toplevel_window, ConfigWindow)


