
from controller.core.xlsx import Xlsx
from view.projects.project import NewProjectWindow
from view.config import Configs as ConfigWindow

import customtkinter
import config

# dev
import copy

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
            corner_radius=0
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
            corner_radius=0
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
            corner_radius=0
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

        dashboard_btn.grid(**self.button_pad, row=0, column=0)
        new_project_btn.grid(**self.button_pad, row=0, column=1)
        projects_btn.grid(**self.button_pad, row=0, column=2)
        config_btn.grid(**self.button_pad, row=0, column=3)

    def do_import(self):

    

        filename = customtkinter.filedialog.askopenfilename(
            initialdir=config.DOCUMENTS_FOLDER,
            title="Selecione uma planilha",
            filetypes=(
                ("Arquivo Excel", "*.xlsx*"),
            )
        )

        if filename:
            xlsx = Xlsx(filename)

            print(xlsx)

    def create_new_project(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = NewProjectWindow(self.master)  # create window if its None or destroyed
            # self.toplevel_window.focus()
            self.toplevel_window.attributes("-topmost", 1)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def change_configs(self):

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ConfigWindow(self.master)  # create window if its None or destroyed
            # self.toplevel_window.focus()
            self.toplevel_window.attributes("-topmost", 1)
        else:
            self.toplevel_window.focus()  # if window exists focus it
