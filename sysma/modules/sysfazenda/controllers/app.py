from controllers.core.web import create_webdriver
from controllers.core.web import webdriver
from controllers.core.recaptcha import ReCaptcha
from controllers.core.xlsx import DataExport

from controllers.core.grabonpage import SFP
from controllers.functionalities.tools import *

from ..models.sysfazenda import SysFazendalConfig, SysFazendaData, SysFazendaHistory

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


FAZENDA_CONSULTA = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Consulta.aspx"

def do_export(path, histoty_id):
    try:
        
        with Session(config.DB_ENGINE) as session:
            sdata: list[SysFazendaData] = session.query(SysFazendaData).filter(SysFazendaData.history_id==histoty_id).all()
            
            with DataExport(path) as data:
                data.export_app_name = "SYSFAZENDA"
                
                data.set_columns([
                    'PLACA',
                    'RENAVAM',
                    'MULTA RENAINF',
                    'IPVA',
                    'DÍVIDA ATIVA',
                    'MULTAS DETRAN',
                    'OUTRAS MULTAS',
                    'DPVAT',
                    'TAXA LICENCIAMENTO',
                ])

                for s in sdata:


                    data.insert_row([
                    s.placa,
                    s.renavam,
                    s.multa_renainf,
                    s.ipva,
                    s.divida_ativa,
                    s.multas_detran,
                    s.outras_multas,
                    s.dpvat,
                    s.taxa_licenciamento,
                    
                ])

        return True
    
    except:
        return False


class SysFazenda(threading.Thread):

    def __init__(
            self,
            threadId: int,
            threadName: str,
            history_id: int,
            project_id: int,
            syspl_data: list,
            view: customtkinter.CTk,
            pb_step: customtkinter.CTkProgressBar, 
            lb_step: customtkinter.CTkLabel, 
            lb_perc: customtkinter.CTkLabel,
        ):

        threading.Thread.__init__(self)

        self.resources = syspl_data

        self.view = view
        self.threadId = threadId
        self.threadName = threadName
        self.pb_step = pb_step
        self.lb_step = lb_step
        self.lb_perc = lb_perc
        self.history_id = history_id
        self.project_id = project_id

        self.driver: webdriver = create_webdriver()

        self.lock_selenium = False

        self.verify_title = lambda x: x.lower() == self.driver.title.strip().lower()
        self.anti_captcha_key = self.get_anti_captcha_key()

    @staticmethod
    def get_anti_captcha_key() -> str:

        with Session(config.DB_ENGINE) as session:
            sysFC = session.query(SysFazendalConfig).one()

        return sysFC.anti_captcha_key if not sysFC is None else sysFC
    
    def run(self):

        balance = ReCaptcha.get_balance(self.anti_captcha_key)

        if balance > 2:
            self.process()
            self.driver.quit()
        else:
            messagebox.showwarning("Balanço Recaptcha", "Saldo abaixo de $2", parent=self.view)
            self.driver.quit()
            self.view.destroy()

        

    
    def record_auto(self, placa: str, renavam: str, auto: SFP = None):
        with Session(config.DB_ENGINE) as session, session.begin():

            h = session.query(SysFazendaHistory).filter(SysFazendaHistory.id == self.history_id).one_or_none()

            if auto:
                session.add(
                    SysFazendaData(
                        history_id=self.history_id,
                        parent_signature=h.signature,
                        placa=placa, 
                        renavam=renavam,
                        ipva=auto.ipva,
                        divida_ativa=auto.divida_ativa,
                        multa_renainf=auto.multas_renainf,
                        multas_detran=auto.multas_detran,
                        outras_multas=auto.outras_multas_sp,
                        dpvat=auto.dpvat,
                        taxa_licenciamento=auto.taxa_licenciamento,
                    )
                )
            else:
                session.add(
                    SysFazendaData(failed=True, placa=placa, renavam=renavam, history_id=self.history_id, parent_signature=h.signature)
                )



    def load_by_renavam_placa(self, placa: str, renavam: str) -> SFP:        

        self.driver.get(FAZENDA_CONSULTA)

        # se não estiver na pagina correta
        if not self.verify_title("Consulta de débitos do veículo"):
            return False

        
        # aguarda até tenha o campo renavam em tela
        wait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "conteudoPaginaPlaceHolder_txtRenavam"))
        )
        
        self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_txtRenavam").send_keys(renavam)
        self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_txtPlaca").send_keys(placa)

        consulta_btn = self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_btn_Consultar")


        if ReCaptcha(self.driver, self.anti_captcha_key).solve(recaptcha_res="g-recaptcha-response"):
            # faz pesquisa
            consulta_btn.click()
            
            try:
                sfp = SFP(self.driver, anti_captcha_key=self.anti_captcha_key)

                if sfp.is_valid:
                    return sfp

            except Exception as e:
                print("err", e)
                self.lb_step.set("Um problema, tentando resolver.")
        

        return None
    
    def process(self):
        self.pb_step.set(0)

        iter_ = 1 / len(self.resources)

        # for each of the cars do:
        for c, auto in enumerate(self.resources, start=1):
            
            if self.lock_selenium:
                return None

            self.lb_step.set(f"[{c} - {len(self.resources)}]")
            

            placa = auto.placa
            renavam = auto.renavam

            percent = (100 * c) // len(self.resources)

            # tentativas
            for i in range(1,5):
                try:
                    
                    _auto = self.load_by_renavam_placa(placa, renavam)

                    if _auto:
                        self.record_auto(placa=auto.placa, renavam=auto.renavam, auto=_auto)
                    else:
                        if i != 5:
                            self.lb_step.set(
                                f"Placa/Renavam ({auto.placa}/{auto.renavam}) sem dados, tentando novamente [{i}*][{c} - {len(self.resources)}]"
                            )
                             
                            continue

                        # caso termine as tentativas, grave com falha no banco
                        self.record_auto(placa=auto.placa, renavam=auto.placa)
                    break
                
                except Exception as e:
                    self.lb_step.set("Erro critico!!!")
                    print(e)
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

        # else:

        #     with Session(config.DB_ENGINE) as session:
        #         failed = \
        #             session.query(SysplData).filter(
        #                 SysplData.history_id == self.history_id, SysplData.failed == True
        #             ).all()
                
        #         if not len(failed):
        #             return None

        #         self.pb_step.set(0)
        #         self.lb_perc.set(f"0%")

        #         iter_ = 1 / len(failed)

        #         for index, auto in enumerate(failed, start=1):
        #             percent = (100 * index) // len(failed)
                    

        #             if self.lock_selenium:
        #                 return None
                    
        #             converted = plate_convert(auto.placa)

        #             self.lb_step.set(f"Reverificando placa {converted} convertida (Mercosul/Tradicional)")
                    
        #             # reprocessar placas

        #             # caso tenha guias abertas, fecha uma
        #             self.close_add_window()

        #             # 5 tentativas para verificar para cada placa
        #             for i in range(1,5):

        #                 try:

        #                     if index % 5 == 0:
        #                         # refaça login a cada 3 placas
        #                         self.relogin()
                            
        #                     new_data = self.load_by_plate(converted)

        #                     if new_data:
        #                         if not new_data.get("veículo_para_leilão_não_encontrado_[mainframe") and new_data.get("dados_veiculo_renavam"):
        #                             self.update_renavam_chassi(session, auto.placa, new_data.get("dados_veiculo_renavam"), new_data.get("dados_veiculo_chassi"))
        #                             self.update_auto(auto, converted, new_data)

        #                         else:
        #                             continue
        #                     else:
        #                         if i != 5:
        #                             self.lb_step.set(f"Placa ({converted}) sem dados, tentando novamente [{i}*][{index} - {len(failed)}]")
        #                             continue
        #                     break
                    
        #                 except Exception as e:
        #                     self.lb_step.set("Erro critico!!!")
        #                     continue
                    
        #             # se carro for concluido atualiza barra de progresso
        #             try:
        #                 self.lb_perc.set(f"{percent}%")
        #                 self.pb_step.set(index*(iter_))

        #             except:
        #                 self.driver.quit()
        #                 break
            
        #         session.commit()
                
        #     export_now = messagebox.askyesno(parent=self.view, title="Finalizado!", message="Deseja exportar agora?")

        #     if export_now:
                
        #         path = customtkinter.filedialog.askdirectory(parent=self.view)

        #         if do_export(path, self.history_id):
        #             messagebox.showinfo(parent=self.view, title="Sucesso", message="Exportação concluida!")

        #         else:
        #             showerror(parent=self.view, title="0", message="Erro na exportação!!!")
        #     # self.view._destroy()
