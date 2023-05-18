from view.base import BaseWindow
from ..controller.app import Syspl

import customtkinter
import time
# import queue

class Worker(BaseWindow):

    def __init__(self, *args, **kwargs):
        
        super().__init__( *args, **kwargs)

        # control vars
        self.lb_perc_var = customtkinter.StringVar(value="0%")

        self.title("Processando...")
        self.resizable(False, False)
        self.center(700, 280)
        self.configure(fg_color=("#fff", "#333"))
        self.draw_title("Processando...")

        self.add_widgets()
        
        self.worker = self.start_worker()


    def add_widgets(self):
        
        lb_conf = {
            "font":customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            "text_color":"#585252",
            # ""
        }

        self.lb_step = customtkinter.CTkLabel(
            self, 
            text="[ 788 - 1000 ]",
            **lb_conf
        )

        self.lb_perc = customtkinter.CTkLabel(
            self,
            textvariable=self.lb_perc_var,
            **lb_conf
        )


        self.pb_step = customtkinter.CTkProgressBar(
            self, 
            width=440, 
            height=10, 
            progress_color="#3B97D3", 
            fg_color="#E0E0E0", 
            mode="determinate" 
        )


        self.btn_stop = customtkinter.CTkButton(
            self,
            text="Parar Pesquisa",
            font=customtkinter.CTkFont(family="Arial", size=12, weight="normal"),
            fg_color="transparent",
            width=143,
            height=30,
            corner_radius=15,
            text_color="#4A4A4A",
            # state="disabled"
        )


        self.lb_step.place(x=314, y=130)
        self.lb_perc.place(x=336, y=174)
        self.btn_stop.place(x=279, y=225)
        self.pb_step.place(x=131, y=159)

    def _destroy(self):

        return super()._destroy()

    def start_worker(self):

        # Syspl is a new thread
        worker = Syspl(
            view=self,
            threadName="Syspl 1",
            threadId=1,
            pb_step=self.pb_step,
            lb_perc=self.lb_perc_var,
            lb_step=self.lb_step,   
        )

        
        worker.start()

        return worker