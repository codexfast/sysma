
from controllers.core.sysmas_resource import LoadSysmaResource
from view.projects.project import NewProjectWindow, ProjectsWindow
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
        # BaseWindow.open_top_level(
        #     self.master, 
        #     self.toplevel_window, 
        #     ProjectsWindow
        # )

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
            command=lambda: \
                BaseWindow.open_top_level(
                    self.master, 
                    self.toplevel_window, 
                    ProjectsWindow
            )
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
        
        

        new_project_btn.grid(**self.button_pad, row=0, column=0)
        projects_btn.grid(**self.button_pad, row=0, column=1)
        config_btn.grid(**self.button_pad, row=0, column=2)


    def create_new_project(self):
        BaseWindow.open_top_level(self.master, self.toplevel_window, NewProjectWindow)

    def change_configs(self):
        BaseWindow.open_top_level(self.master, self.toplevel_window, ConfigWindow)


