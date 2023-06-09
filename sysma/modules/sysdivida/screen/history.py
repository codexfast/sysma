from view.base import BaseWindow
from ..models.sysdivida import SysDividaHistory, SysDividaData
from ..controllers.app import do_export

from tkinter import ttk
from tkinter import messagebox, filedialog

import customtkinter
import config

from sqlalchemy.orm import Session

class History(BaseWindow):

    def __init__(self, master, project_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title("Histórico")
        self.resizable(False, False)

        self.project_id = project_id
        # self.center(400, 600)

        self.add_widgets()

    def add_widgets(self):

        def item_selected(event):
            
            item = tree.item(tree.focus())
            _id = item['values'][0]

            with Session(config.DB_ENGINE) as session:
                data = session.query(SysDividaData)\
                    .filter(SysDividaData.history_id==_id and SysDividaData.failed==False).all()
                
                if data:
                    export = messagebox.askyesno("Exportar", "Exportar agora?", parent=self)

                    if export:
                        
                        path = filedialog.askdirectory(parent=self)

                        if do_export(path, _id):
                            messagebox.showinfo(parent=self, title="Sucesso", message="Exportação concluida!")

                        else:
                            messagebox.showerror(parent=self.view, title="0", message="Erro na exportação!!!")


                else:
                    messagebox.showerror("Erro", f"SYSDIVIDA #{_id} - no row for \"sysdividahistory\"", parent=self)



        columns = ("id", "app", "datetime")

        tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        tree.heading("id", text="ID", anchor="w")
        tree.heading("app", text="APP", anchor="w")
        tree.heading("datetime", text="DATETIME", anchor="w")

        with Session(config.DB_ENGINE) as session:

            historical = session.query(SysDividaHistory).filter(SysDividaHistory.project_id==self.project_id).all()

            for h in historical:
                tree.insert('', customtkinter.END, values=(h.id, "SYSDIVIDA", h.time_created))

        tree.bind("<Double-Button-1>", item_selected)

        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = customtkinter.CTkScrollbar(self, command=tree.yview, orientation="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree.configure(yscroll=scrollbar.set)
