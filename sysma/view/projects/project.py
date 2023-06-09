from view.base import BaseWindow, BaseForm
# from modules.syspl.view import View as SysplView
from modules.syspl.screen.history import History as SysplHis
from modules.sysfazenda.screen.history import History as SysfazendaHis 
from modules.sysdivida.screen.history import History as SysdividaHis
from modules.syspl.models.syspl import SysplLogin, SysplData, SysplHistory

from controllers.core.xlsx import DataExport

from config import Images, DB_ENGINE, DOCUMENTS_FOLDER
from controllers.functionalities.import_export_xlsx import do_import

from tkcalendar import Calendar

import customtkinter

from tkinter.messagebox import showerror, showinfo
from datetime import datetime

from sqlalchemy.orm import Session
from models.projects import Projects

from modules.sysdivida.controllers.app import check_input_dividas


from modules.sysdivida.screen.worker import Worker as SysDivida
from modules.sysfazenda.screen.worker import Worker as SysFazendaWorker
from modules.syspl.screen.worker import Worker as SysplWorker


from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


class _C(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Calendário")
        self.resizable(False, False)
        self.center(400, 400)

        self.calendarvar = None

        self.calendar = Calendar(self, locale="pt_BR")
        self.calendar.pack(expand=True, fill=customtkinter.BOTH)

        self.bind("<<CalendarSelected>>", self.set_date)

    def set_date(self, event):
        self.calendarvar.set(self.calendar.get_date())
        self.destroy()
        self.master.deiconify()

class NewProjectWindow(BaseWindow):

    """
    projeto contém:
    - 
    - 
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Projeto")
        self.center(750,425)
        self.resizable(False, False)
        self.configure(fg_color=("#fff", "#333"))
        self.draw_title("Criar novo projeto")

        self.calendarvar = customtkinter.StringVar(value="Data de Início")

        self.add_widgets()

    def add_widgets(self):

        calendarimg = Images.BTN_CALENDAR

        # entries
        self.name = BaseForm.entry(self, width=300, placeholder="Nome")
        self.leiloeiro = BaseForm.entry(self, width=330, placeholder="Leiloeiro")
        self.patio = BaseForm.entry(self, width=330, placeholder="Pátio")
        self.estado = BaseForm.entry(self, width=119, placeholder="Estado")
        self.endereco = BaseForm.entry(self, width=370, placeholder="Endereço")
        self.cidade = BaseForm.entry(self, width=260, placeholder="Cidade")
        self.descricao = BaseForm.entry(self, width=670, placeholder="Descreva sobre o projeto (Opcional)")


        # button
        self.date_start = BaseForm.buttonv2(self, 100, 40, calendarimg, self.calendarvar, self.open_calendar)
        self.create_btn = BaseForm.button(self, "Criar", command=self.create_project)

        # Places
        self.name.place(x=40, y=103)
        self.leiloeiro.place(x=380, y=103)
        self.date_start.place(x=40, y=160)
        self.patio.place(x=221, y=160)
        self.estado.place(x=591, y=160)
        self.endereco.place(x=40, y=217)
        self.cidade.place(x=450, y=217)
        self.descricao.place(x=40, y=274)

        self.create_btn.place(x=605, y=355)

    def create_project(self):
        
        def extract_date(str):
            _format = "%d/%m/%Y"

            try:
                date = datetime.strptime(str, _format)

                return date
            
            except ValueError:
                return None


        data = {
            "name" : self.name.get(),
            "leiloeiro" : self.leiloeiro.get(),
            "date_start" : extract_date(self.calendarvar.get()),
            "patio" : self.patio.get(),
            "estado" : self.estado.get(),
            "endereco" : self.endereco.get(),
            "cidade" : self.cidade.get(),
            "descricao" : self.descricao.get(),
        }
        

        if data["name"] and data["leiloeiro"] and data["date_start"] and data["patio"]:
            
            path = self.attach_file()
            
            if path:

                with Session(DB_ENGINE) as session:

                    p = Projects(**data)
                    
                    session.add(p)
                    session.commit()
                    session.refresh(p)
                    # session.flush()

                    # if not do_import(filename=path, project_id=p.id, parent=self):
                    #     session.rollback()
                    # else:
                    #     session.commit()

                    r = do_import(filename=path, project_id=p.id, parent=self)


                    showinfo(parent=self, title="Projeto", message="Projeto criado com sucesso!")
                    self._destroy()

        
        else:
            showerror(parent=self, title="0", message="Dados importantes não preenchidos!")

        # print(name, leiloeiro, date_start, patio, estado, endereco, cidade, descricao, sep='|')
        # print(len(descricao))

    def attach_file(self):
    
        return filedialog.askopenfilename(
            parent=self,
            initialdir=DOCUMENTS_FOLDER,
            title="Selecione uma planilha",
            filetypes=(
                ("Arquivo Excel", "*.xlsx*"),
            ),

        )

    def open_calendar(self):
        pick_calendar = _C(self)
        pick_calendar.calendarvar = self.calendarvar

class ProjectsWindow(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.toplevel_window = None

        self.title("Projetos")
        self.resizable(False, False)

        self.add_widgets()

    def add_widgets(self):
        def item_selected(event):
            
            item = tree.item(tree.focus())
            _id = item['values'][0]

            BaseWindow.open_top_level(self, self.toplevel_window, ProjectManagerWindow, project_id=_id)

        columns = (
            "id",
            "name",
            "date_start",
            "status"
        )

        tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        tree.heading("id", text="ID", anchor="w")
        tree.column("id", minwidth=25, width=30, stretch=False)

        tree.heading("name", text="NOME", anchor="w")
        tree.column("name", minwidth=100, width=300, stretch=True)

        tree.heading("date_start", text="INICIADO EM", anchor="w")
        tree.column("date_start", width=130)

        tree.heading("status", text="STATUS", anchor="w")
        tree.column("status", width=130)


        with Session(DB_ENGINE) as session:

            projects = session.query(Projects).all()

            for p in projects:
                tree.insert('', customtkinter.END, values=(p.id, p.name, p.date_start, "ABERTO" if not p.finished_at else "FECHADO"))

        tree.bind("<Double-Button-1>", item_selected)
        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = customtkinter.CTkScrollbar(self, command=tree.yview, orientation="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree.configure(yscroll=scrollbar.set)

class ProjectManagerWindow(BaseWindow):
    def __init__(self, master, project_id: int, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.data = self.__load(project_id)
    
        self.toplevel_window = None


        self.configure(fg_color="#fff")
        self.resizable(False, False)
        self.title(f'Projeto #{self.data.id} - {"ABERTO" if not self.data.finished_at else "FECHADO"}')
        self.draw_title(self.data.name)
        self.center(height=387, width=700)

        self.add_widgets()

    def add_widgets(self):
        sub_lb = customtkinter.CTkLabel(
			self,
            text="Selecione um módulo",
            font=customtkinter.CTkFont(family="Arial", size=13),
            text_color="#A6A6A6",
            
		)

        ball_styles = {
            "height": 6,
            "width": 6,
            "fg_color":"#C9C9C9",
            "corner_radius":50
        }

        ball_sep1 = customtkinter.CTkFrame(self, **ball_styles)
        ball_sep2 = customtkinter.CTkFrame(self, **ball_styles)

        mod1 = BaseForm.buttonv3(
            self,
            96,
            126,
            image=Images.SYSPL,
            command=self.open_syspl_worker
        )

        mod2 = BaseForm.buttonv3(
            self,
            96,
            126,
            image=Images.SYSFAZENDA,
            command=self.open_sysfazenda_worker
        )

        mod3 = BaseForm.buttonv3(
            self,
            96,
            126,
            image=Images.SYSDIVIDA,
            command=self.open_sysdivida_worker
        )

        his_syspl = BaseForm.buttonv3(
            self,
            21,
            12,
            image=Images.FOLDERCHECK,
            command=lambda: \
                BaseWindow.open_top_level(self, self.toplevel_window, SysplHis, project_id=self.data.id)
        )

        his_fazenda = BaseForm.buttonv3(
            self,
            21,
            12,
            image=Images.FOLDERCHECK,
            command=lambda: \
                BaseWindow.open_top_level(self, self.toplevel_window, SysfazendaHis, project_id=self.data.id)
        )

        his_divida = BaseForm.buttonv3(
            self,
            21,
            12,
            image=Images.FOLDERCHECK,
            command=lambda: \
                BaseWindow.open_top_level(self, self.toplevel_window, SysdividaHis, project_id=self.data.id)
        )

        # places
        sub_lb.place(x=287, y=75)
        
        mod1.place(x=166, y=130)
        mod2.place(x=302, y=130)
        mod3.place(x=438, y=130)

        his_syspl.place(x=203, y=272)
        his_fazenda.place(x=340, y=272)
        his_divida.place(x=475, y=272)

        ball_sep1.place(x=279, y=190)
        ball_sep2.place(x=415, y=190)


    def __load(self, _id):
        with Session(DB_ENGINE) as session:
            return session.query(Projects).filter(Projects.id==_id).one()
        

    def open_syspl_worker(self):

        with Session(DB_ENGINE) as session:

            login_syspl:SysplLogin = session.query(SysplLogin).one_or_none()

            if login_syspl:
                if login_syspl.username and login_syspl.password:
                    BaseWindow.open_top_level(self, self.toplevel_window, SysplWorker, project_id=self.data.id)

                    return;

            return messagebox.showwarning("Atenção", "Verifique os dados de login do sispl para continuar!", parent=self)
    
    def open_sysfazenda_worker(self):

        with Session(DB_ENGINE) as session:
            
            last_history = session.query(SysplHistory).filter(SysplHistory.project_id == self.data.id).order_by(SysplHistory.id.desc()).first()

            syspl_data = \
                session.query(SysplData)\
                    .filter(SysplData.history_id == last_history.id, SysplData.failed == False).all()\
                            if not last_history is None else []
                
            if syspl_data:
                BaseWindow.open_top_level(self, self.toplevel_window, SysFazendaWorker, project_id=self.data.id, syspl_data=syspl_data)
            else:
                messagebox.showwarning("Sysfazenda", "Sem dados para processar com 'SysFazenda'", parent=self)

    def open_sysdivida_worker(self):
        with Session(DB_ENGINE) as session:
            
            # pega ultimo historico
            last_history = session.query(SysplHistory).filter(SysplHistory.project_id == self.data.id).order_by(SysplHistory.id.desc()).first()

            # pega ultimas pesquisas com id de historico especifico
            syspl_data = \
                session.query(SysplData)\
                    .filter(SysplData.history_id == last_history.id, SysplData.failed == False).all()\
                            if not last_history is None else []
            
            if syspl_data:

                # Pergunta se pode exportar planilha de preenchimento para usar posteriormente    
                if messagebox.askyesno("Template", "Exportar tabela de preenchimento \"SysDivida\"?", parent=self):
                    path = filedialog.askdirectory(**self.DEFAULT_SELECT_FOLDER)

                    if path:                
                        with DataExport(path) as data:
                            data.export_app_name = "dvidas_preenchimento".upper()

                            data.set_columns([
                                "LOTE",
                                "PLACA",
                                "RENAVAM",
                                "VALOR",
                            ])

                            for s in syspl_data:
                                data.insert_row([
                                    "0000",
                                    s.placa,
                                    s.renavam,
                                    0.00
                                ])

                        messagebox.showinfo("Sucesso", "Exportado com sucesso!", parent=self)


                # Importa planilha preenchida com dados nescessarios
                if messagebox.askokcancel("Processamento", "Informe destino da tabela preenchida com lote, placa, renavam e valor \"SysDivida\"", parent=self):
                    # aqui pega o path da tabela preenchida

                    file_path = filedialog.askopenfilename(**self.DEFAULT_OPEN_XLSX)
                    
                    if file_path:

                        # checa se é valido a planilha preenchida
                        assets = check_input_dividas(file_path, syspl_data)
                        
                        if assets:
                            BaseWindow.open_top_level(self, self.toplevel_window, SysDivida, project_id=self.data.id, syspl_data=syspl_data)

                        else:
                            messagebox.showerror("ValueError", "Há dados que nao conferem", parent=self)
                
            else:
                messagebox.showwarning("Sysdivida", "Sem dados para processar com 'SysDivida'", parent=self)