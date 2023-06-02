from view.base import BaseWindow
from ..controllers.app import Syspl
from ..models.syspl import SysplHistory

from sqlalchemy.orm import Session

import customtkinter
import time
import config
# import queue

class Worker(BaseWindow):

    def __init__(self, master, project_id: int, *args, **kwargs):
        
        super().__init__(master, *args, **kwargs)

        # control vars
        self.lb_perc_var = customtkinter.StringVar(value="0%")
        self.lb_step_var = customtkinter.StringVar(value="[0000 - 0000]")

        self.project_id = project_id

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
            textvariable=self.lb_step_var,
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
            command=self._destroy
            # state="disabled"
        )


        self.pb_step.place(relx=.5, y=159, anchor="center")
        self.lb_perc.place(relx=.5, y=184, anchor="center")
        self.lb_step.place(relx=.5, y=130, anchor="center")
        self.btn_stop.place(relx=.5, y=225, anchor="center")

    def _destroy(self):
        self.worker.lock_selenium = True
        return super()._destroy()

    def create_history(self) -> int:

        with Session(config.DB_ENGINE) as session:
            
            history = SysplHistory(project_id=self.project_id)

            session.add(history)
            
            session.commit()
            session.refresh(history)

            return history.id



    def start_worker(self):

        
        # Syspl is a new thread
        worker = Syspl(
            view=self,
            threadName="Syspl 1",
            threadId=1,
            history_id=self.create_history(),
            pb_step=self.pb_step,
            lb_perc=self.lb_perc_var,
            lb_step=self.lb_step_var,
            project_id=self.project_id
        )

        
        worker.start()

        return worker