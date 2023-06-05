from controllers.core.web import create_webdriver
from controllers.core.web import webdriver
from controllers.data import Resources
from controllers.core.xlsx import DataExport
from controllers.functionalities.tools import *

from ..models.syspl import SysplData
from ..models.syspl import SysplLogin

from sqlalchemy.orm import Session

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from tkinter.messagebox import showerror
from tkinter import messagebox

import customtkinter
import time
import threading
import dataclasses
import config


PATIO_LOGIN = "https://www.sispl.sp.gov.br/maximo/webclient/login/login.jsp"
PATIO_CONSULTA = "https://www.sispl.sp.gov.br/maximo/ui/?event=loadapp&value=ms_rptauc01&uisessionid=219&_tt=c8l2njvugsgco33oknltqkj2jf"


def do_export(path, histoty_id):

    try:
        
        with Session(config.DB_ENGINE) as session:
            sdata = session.query(SysplData).filter(SysplData.history_id==histoty_id).all()
            
            with DataExport(path) as data:
                
                data.set_columns([
                    'PLACA',
                    'NOME FINANCEIRA',
                    'VIGENCIA DE CONTRATO',
                    'RESTRIÇÃO I',
                    'COMUN. VENDA DATA DE INCL.',
                    'BLOQ. DE GUINCHO',
                    'ÚLTIMO LICENCIAMENTO',
                    
                    'BLOQ. I TIPO',
                    'BLOQ. I DATA INCL.',
                    'BLOQ. I DESC.',
                    'BLOQ. II TIPO',
                    'BLOQ. II DATA INCL.',
                    'BLOQ. II DESC.',
                    'BLOQ. III TIPO',
                    'BLOQ. III DATA INCL.',
                    'BLOQ. III DESC.',
                    'BLOQ. IV TIPO',
                    'BLOQ. IV DATA INCL.',
                    'BLOQ. IV DESC.',
                ])

                for s in sdata:


                    data.insert_row([
                    s.placa,
                    s.finaceira_nome,
                    s.finaceira_vigencia_do_contrato,
                    s.dados_veiculo_restricao_1,
                    s.comun_venda_data_da_inclusao,
                    s.dados_veiculo_bloqueio_de_guincho,
                    s.dados_veiculo_ultimo_licenciamento,
                    
                    s.bloqueio_1_tipo,
                    s.bloqueio_1_data_inclusao,
                    s.bloqueio_1_descricao,
                    s.bloqueio_2_tipo,
                    s.bloqueio_2_data_inclusao,
                    s.bloqueio_2_descricao,
                    s.bloqueio_3_tipo,
                    s.bloqueio_3_data_inclusao,
                    s.bloqueio_3_descricao,
                    s.bloqueio_4_tipo,
                    s.bloqueio_4_data_inclusao,
                    s.bloqueio_4_descricao,
                    
                ])

        return True
    
    except:
        return False
    
@dataclasses.dataclass
class Auto:
    pass


class Syspl(threading.Thread):

    def __init__(
            self,
            threadId: int,
            threadName: str,
            history_id: int,
            project_id: int,
            view: customtkinter.CTk,
            pb_step: customtkinter.CTkProgressBar, 
            lb_step: customtkinter.CTkLabel, 
            lb_perc: customtkinter.CTkLabel,
        ):

        threading.Thread.__init__(self)

        self.resources = Resources(project_id=project_id)

        self.view = view
        self.threadId = threadId
        self.threadName = threadName
        self.pb_step = pb_step
        self.lb_step = lb_step
        self.lb_perc = lb_perc
        self.history_id = history_id

        self.driver: webdriver = create_webdriver()

        self.lock_selenium = False

        self.verify_title = lambda x: x.lower() == self.driver.title.lower()

    def run(self):
        self.process()
    

    def do_login(self):

        self.driver.get(PATIO_LOGIN)

        with Session(config.DB_ENGINE) as session: 
            login = session.query(SysplLogin).one_or_none()

            # Encontra input usuario e preenche com login
            # self.driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(login.username)
            self.driver.find_element(By.XPATH, '//*[@id="username"]').send_keys("36490625857")

            # Encontra input senha e preenche com senha
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("rennan10")
            # self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(login.password)


        # envia input
        clickable = self.driver.find_element(By.XPATH, '//*[@id="loginbutton"]')
        clickable.click()


        try:
            self.driver.find_element(By.ID, "titlebar-tb_appname")

        except NoSuchElementException:
    
            return False

        return self.driver.current_url
    
    def relogin(self):

        try:

            btn = wait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "titlebar_hyperlink_8-lbsignout"))
            )

            btn.click()

        except NoSuchElementException:
            return False

        finally:
            return self.do_login()
        
    def close_add_window(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as err:
            # caso nao tenha conseguido fechar a guia adicional
            pass

    def load_by_plate(self, plate: str) -> dict:
        """Busca pela placa do carro, necessário fazer login antes de executar esta função"""

        self.driver.get(PATIO_CONSULTA)

        
        # se não estiver na pagina correta
        if not self.verify_title("Consulta de Leiloeiros"):
            return False
        

        try:

            btn = wait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "m324bb57f-pb"))
            )
            btn.click()

        except NoSuchElementException as err:
            print(err)

        # time.sleep(1.5)

        wait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "m6631cd9c-tb"))
        ).send_keys(plate)

        wait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "m2bf96c97-pb"))
        ).click()


        time.sleep(1.5)
        # time.sleep(3.5)

        if wait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it("mf36f9253-rtv")):
            body = self.driver.find_element(By.XPATH, '/html/body')

            obj = {}
            prefix: str = ""

            for i in body.text.split('\n'):
                try:

                    key, value, *_ = i.split(':')

                    # print(f"{prefix}{key} -> {value}")

                    key = key.replace(" ", "_")


                    obj[f'{prefix}{key.lower()}'] = str(value).strip() if value else None

                except:
                    if i == "Bloqueio 1":
                        prefix = "bloqueio_1_"

                    elif i == "Bloqueio 2":
                        prefix = "bloqueio_2_"

                    elif i == "Bloqueio 3":
                        prefix = "bloqueio_3_"

                    elif i == "Bloqueio 4":
                        prefix = "bloqueio_4_"

                    elif i == "Dados do Veículo":
                        prefix = "dados_veiculo_"

                    elif i == "Proprietário":
                        prefix = "proprietario_"
                    
                    elif i == "Comunicação de Venda":
                        prefix = "comun_venda_"

                    elif i == "Financeira":
                        prefix = "finaceira_"

                    elif i == "BIN/Motor":
                        prefix = "bin_motor_"

                    else:
                        prefix = ""


        # result: list = []
        
        # result = [
        #     obj.get('dados_veiculo_placa'),
        #     obj.get('finaceira_nome'),
        #     obj.get('finaceira_vigência_do_contrato'),
        #     obj.get('dados_veiculo_restrição_1'),
        #     obj.get('comun_venda_data_da_inclusão'),
        #     obj.get('dados_veiculo_bloqueio_de_guincho'),
        #     obj.get('dados_veiculo_último_licenciamento'),

        #     obj.get('bloqueio_1_tipo'),
        #     obj.get('bloqueio_1_data_inclusão'),
        #     obj.get('bloqueio_1_descrição'),
        #     obj.get('bloqueio_2_tipo'),
        #     obj.get('bloqueio_2_data_inclusão'),
        #     obj.get('bloqueio_2_descrição'),
        #     obj.get('bloqueio_3_tipo'),
        #     obj.get('bloqueio_3_data_inclusão'),
        #     obj.get('bloqueio_3_descrição'),
        #     obj.get('bloqueio_4_tipo'),
        #     obj.get('bloqueio_4_data_inclusão'),
        #     obj.get('bloqueio_4_descrição'),

        # ]


        time.sleep(1.5)
        
        self.driver.switch_to.default_content();

        return obj
    
    def update_auto(self, auto: SysplData, new_placa, new_data):
            
            auto.placa=new_placa
            auto.finaceira_nome=new_data.get("finaceira_nome")
            auto.finaceira_vigencia_do_contrato=new_data.get("finaceira_vigência_do_contrato")
            auto.dados_veiculo_restricao_1=new_data.get("dados_veiculo_restrição_1")
            auto.comun_venda_data_da_inclusao=new_data.get("comun_venda_data_da_inclusão")
            auto.dados_veiculo_bloqueio_de_guincho=new_data.get("dados_veiculo_bloqueio_de_guincho")
            auto.dados_veiculo_ultimo_licenciamento=new_data.get("dados_veiculo_último_licenciamento")

            auto.bloqueio_1_tipo = new_data.get("bloqueio_1_tipo")
            auto.bloqueio_1_data_inclusao = new_data.get("bloqueio_1_data_inclusão")
            auto.bloqueio_1_descricao = new_data.get("bloqueio_1_descrição")

            auto.bloqueio_2_tipo = new_data.get("bloqueio_2_tipo")
            auto.bloqueio_2_data_inclusao = new_data.get("bloqueio_2_data_inclusão")
            auto.bloqueio_2_descricao = new_data.get("bloqueio_2_descrição")

            auto.bloqueio_3_tipo = new_data.get("bloqueio_3_tipo")
            auto.bloqueio_3_data_inclusao = new_data.get("bloqueio_3_data_inclusão")
            auto.bloqueio_3_descricao = new_data.get("bloqueio_3_descrição")

            auto.bloqueio_4_tipo = new_data.get("bloqueio_4_tipo")
            auto.bloqueio_4_data_inclusao = new_data.get("bloqueio_4_data_inclusão")
            auto.bloqueio_4_descricao = new_data.get("bloqueio_4_descrição")
    
            auto.failed = False

    def record_auto(self, auto: Auto = {}, placa=None):
        
        with Session(config.DB_ENGINE) as session, session.begin():
            
            # se tiver algum valor diferente de 'None'
            if len(
                list(
                    filter(
                        lambda x: x!=None, list(auto.values())
                    )
                )
            ):

                session.add(SysplData(
                    history_id=self.history_id,
                    placa=placa,
                    finaceira_nome=auto.get("finaceira_nome"),
                    finaceira_vigencia_do_contrato=auto.get("finaceira_vigência_do_contrato"),
                    dados_veiculo_restricao_1=auto.get("dados_veiculo_restrição_1"),
                    comun_venda_data_da_inclusao=auto.get("comun_venda_data_da_inclusão"),
                    dados_veiculo_bloqueio_de_guincho=auto.get("dados_veiculo_bloqueio_de_guincho"),
                    dados_veiculo_ultimo_licenciamento=auto.get("dados_veiculo_último_licenciamento"),

                    bloqueio_1_tipo = auto.get("bloqueio_1_tipo"),
                    bloqueio_1_data_inclusao = auto.get("bloqueio_1_data_inclusão"),
                    bloqueio_1_descricao = auto.get("bloqueio_1_descrição"),

                    bloqueio_2_tipo = auto.get("bloqueio_2_tipo"),
                    bloqueio_2_data_inclusao = auto.get("bloqueio_2_data_inclusão"),
                    bloqueio_2_descricao = auto.get("bloqueio_2_descrição"),

                    bloqueio_3_tipo = auto.get("bloqueio_3_tipo"),
                    bloqueio_3_data_inclusao = auto.get("bloqueio_3_data_inclusão"),
                    bloqueio_3_descricao = auto.get("bloqueio_3_descrição"),

                    bloqueio_4_tipo = auto.get("bloqueio_4_tipo"),
                    bloqueio_4_data_inclusao = auto.get("bloqueio_4_data_inclusão"),
                    bloqueio_4_descricao = auto.get("bloqueio_4_descrição"),
                ))
            
            else:
                session.add(SysplData(
                    history_id=self.history_id,
                    placa=placa if not placa is None else "xxxxxxx",
                    failed=True
                ))

    def process(self):
        self.pb_step.set(0)

        iter_ = 1 / len(self.resources)

        # first do login on web page
        if not self.do_login():
            showerror("Erro no login", "Usuário ou senhas incorretas", parent=self.view)

            self.driver.close()
            self.view._destroy()


        # for each of the cars do:
        for c, auto in enumerate(self.resources.get_autos(), start=1):

            if self.lock_selenium:
                return None

            self.lb_step.set(f"[{c} - {len(self.resources)}]")
            

            placa = auto.placa
            percent = (100 * c) // len(self.resources)

            # caso tenha guias abertas, fecha uma
            self.close_add_window()

            for i in range(1,5):

                try:

                    if c % 5 == 0:
                        self.relogin()
                    
                    _auto = self.load_by_plate(placa)

                    if _auto:
                        if not _auto.get("veículo_para_leilão_não_encontrado_[mainframe"):
                            self.record_auto(_auto, placa=auto.placa)
                        else:
                            self.record_auto(placa=auto.placa)


                    else:
                        if i != 5:
                            self.lb_step.set(f"Placa ({auto.placa}) sem dados, tentando novamente [{i}*][{c} - {len(self.resources)}]")
                            continue

                        # caso termine as tentativas, grave com falha no banco
                        self.record_auto(placa=auto.placa)
                    break
                
                except Exception as e:
                    self.lb_step.set("Erro critico!!!", e)
                    continue

            # se carro for concluido atualiza barra de progresso
            try:
                self.lb_perc.set(f"{percent}%")
                self.pb_step.set(c*(iter_))

            except:
                self.driver.quit()
                break
            
            # sempre no final
            self.view.update()

        else:

            with Session(config.DB_ENGINE) as session:
                failed = \
                    session.query(SysplData).filter(
                        SysplData.history_id == self.history_id, SysplData.failed == True
                    ).all()
                
                if not len(failed):
                    return None

                self.pb_step.set(0)
                self.lb_perc.set(f"0%")

                iter_ = 1 / len(failed)

                for index, auto in enumerate(failed, start=1):
                    percent = (100 * index) // len(failed)
                    

                    if self.lock_selenium:
                        return None
                    
                    converted = plate_convert(auto.placa)

                    self.lb_step.set(f"Reverificando placa {converted} convertida (Mercosul/Tradicional)")
                    
                    # reprocessar placas

                    # caso tenha guias abertas, fecha uma
                    self.close_add_window()

                    # 5 tentativas para verificar para cada placa
                    for i in range(1,5):

                        try:

                            if index % 5 == 0:
                                # refaça login a cada 3 placas
                                self.relogin()
                            
                            new_data = self.load_by_plate(converted)

                            if new_data:
                                if not new_data.get("veículo_para_leilão_não_encontrado_[mainframe") and new_data.get("dados_veiculo_renavam"):
                                    
                                    self.update_auto(auto, converted, new_data)

                            else:
                                if i != 5:
                                    self.lb_step.set(f"Placa ({converted}) sem dados, tentando novamente [{i}*][{index} - {len(failed)}]")
                                    continue
                            break
                    
                        except Exception as e:
                            self.lb_step.set("Erro critico!!!")
                            continue
                    
                    # se carro for concluido atualiza barra de progresso
                    try:
                        self.lb_perc.set(f"{percent}%")
                        self.pb_step.set(index*(iter_))

                    except:
                        self.driver.quit()
                        break
            
                session.commit()
                
            export_now = messagebox.askyesno(parent=self.view, title="Finalizado!", message="Deseja exportar agora?")

            if export_now:
                
                path = customtkinter.filedialog.askdirectory(parent=self.view)

                if do_export(path, self.history_id):
                    messagebox.showinfo(parent=self.view, title="Sucesso", message="Exportação concluida!")

                else:
                    showerror(parent=self.view, title="0", message="Erro na exportação!!!")
            # self.view._destroy()
