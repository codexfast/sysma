import os
import abc
import typing
import datetime
import dataclasses

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from controllers.core.recaptcha import ReCaptcha
from controllers.functionalities.tools import selecionar_contas

def custom_to_float(_str: typing.AnyStr) -> float:
    _ = _str.replace('.', '')
    _ = _.replace(',', '.')

    try: 
        return float(_)

    except ValueError:
        return float()

@dataclasses.dataclass
class GrabOnPage(abc.ABC):
    driver: webdriver.Chrome = dataclasses.field(repr=False)

    def grab_text(self, by: typing.AnyStr, value: typing.AnyStr, default = None) -> WebElement:
        try:
            text = self.driver.find_element(by, value).text

            return text if text else default

        except NoSuchElementException:
            return default

    def has_elmt(self, by: typing.AnyStr, value: typing.AnyStr) -> bool:
        return bool(len(self.driver.find_elements(by, value)))

    def extract_float_from_table(self, elmt: WebElement) -> typing.Dict:
        _pre_dict = {}

        def _(m: WebElement) -> typing.Dict:
            td = m.find_elements(By.TAG_NAME, "td")
            _r = {}

            _t = td[4].text.replace('.', '')
            _t = _t.replace(',', '.')

            try:
                _r[td[0].text] = float(_t)
            except ValueError:
                _r[td[0].text] = 0.00

            return _r

        try:
            for i in elmt.find_elements(By.TAG_NAME, "tr"):
                
                _pre_dict = {**_pre_dict, **_(i)}
        except:
            pass

        return _pre_dict

    def extract_float_from_table_ipva(self, elmt: WebElement) -> typing.Dict:
        _pre_dict = {}

        def _(m: WebElement) -> typing.Dict:
            td = m.find_elements(By.TAG_NAME, "td")
            _r = {}

            try:

                _t = td[4].text.replace('.', '')
                _t = _t.replace(',', '.')
            
            except:
                _t = 0


            try:
                _r[td[0].text] = float(_t)
            except ValueError:
                _r[td[0].text] = 0.00

            return _r

        try:
            for i in elmt.find_elements(By.TAG_NAME, "tr"):
                _pre_dict = {**_pre_dict, **_(i)}
        except Exception as err:
            print(err, "<- erro Ignorado")

        return _pre_dict

@dataclasses.dataclass
class Licenciamento(GrabOnPage):
    total_licenciamento: float = dataclasses.field(default_factory=float)

    def __post_init__(self):
        year_actual = datetime.date.today().year
        year_prev = datetime.date.today().year + 1

        _ = self.extract_float_from_table(self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_tbTaxasDetalhe"))
        keys = _.keys()

        if f'Licenciamento {year_prev}' in keys:
            for i in keys:
                if "Licenciamento" in i:
                    if str(year_prev) in i:
                        continue

                    self.total_licenciamento += _[i]
        else:
            for i in keys:
                if "Licenciamento" in i:
                    if str(year_actual) in i:
                        continue

                    self.total_licenciamento += _[i]

@dataclasses.dataclass
class Ipva(GrabOnPage):

    ipva: float = dataclasses.field(default_factory=float)

    def __post_init__(self):
        default = 0.00
        year_actual = datetime.date.today().year

        _ = self.extract_float_from_table_ipva(self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_tbIpvaPend"))

        for y in range(2000, year_actual + 1):
            self.ipva += round(_.get(str(y), default), ndigits=2)

@dataclasses.dataclass
class Multas(GrabOnPage):

    detran: float = dataclasses.field(default_factory=float)
    renainf: float = dataclasses.field(default_factory=float)
    outras_multas: float = dataclasses.field(default_factory=float)


    def __post_init__(self):
        default = 0.00
        _ = self.extract_float_from_table(self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_tbMultaResumo"))
        
        self.detran = _.get('DETRAN', default)
        self.renainf= _.get('RENAINF', default)
        
        municipal = _.get('MUNICIPAL', default)
        convenio = _.get('CONVENIO', default)
        der = _.get('D.E.R.', default)

        self.outras_multas = round(municipal + convenio + der, ndigits=2)

@dataclasses.dataclass
class MultasDetalhadas(GrabOnPage):


    detran: float = dataclasses.field(default_factory=float)
    renainf: float = dataclasses.field(default_factory=float)
    outras_multas: float = dataclasses.field(default_factory=float)
    detalhamento: typing.List[typing.Dict] = dataclasses.field(default_factory=list)


    def __post_init__(self):
        default = 0.00
        _ = self.extract_float_from_table(self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_tbMultaResumo"))
        
        self.detran = _.get('DETRAN', default)
        self.renainf= _.get('RENAINF', default)
        
        municipal = _.get('MUNICIPAL', default)
        convenio = _.get('CONVENIO', default)
        der = _.get('D.E.R.', default)

        self.outras_multas = round(municipal + convenio + der, ndigits=2)

        if self.has_elmt(By.ID, "conteudoPaginaPlaceHolder_btnDetalharMultas"):

            # Vai a sessão de multas detalhadas
            self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_btnDetalharMultas").click()

            # Captura as multas uma a uma
            self.detalhamento = self.grab_details_debt()

            # Retorna a pagina principal dos dados
            self.driver.back()

        else: self.detalhamento = []

        

    def grab_details_debt(self) -> typing.List[typing.Dict]:
        _final = []

        target_child = self.driver.find_element(By.ID, "conteudoPaginaPlaceHolder_trMultaCab")
        target = target_child.find_element(By.XPATH, "..")

        rows = target.find_elements(By.TAG_NAME, "tr")
        del rows[-1]

        for i in range(0, len(rows), 5):

            second_tr = rows[i+2]
            third_tr = rows[i+3]
            fourth_tr = rows[i+4]

            value = custom_to_float(
                third_tr.find_elements(By.TAG_NAME, "td")[5].text.replace('R$','')
            )

            _final.append(
                {
                    'name': fourth_tr.find_elements(By.TAG_NAME, "td")[3].text,
                    'guia': third_tr.find_elements(By.TAG_NAME, "td")[3].text,
                    'ait': second_tr.find_elements(By.TAG_NAME, "td")[3].text,
                    'value': value
                }
            )
        
        return _final


@dataclasses.dataclass
class SFPDividas(GrabOnPage):
    anti_captcha_key: str

    balance: float
    lote: typing.AnyStr

    is_valid: bool = False

    renavam:            typing.AnyStr = None # OK
    placa:              typing.AnyStr = None # Ok
    ipva:               typing.AnyStr = None # OK
    divida_ativa:       typing.AnyStr = None # OK
    multas_renainf:     typing.AnyStr = None # OK
    multas_detran:      typing.AnyStr = None # Ok
    outras_multas_sp:   typing.AnyStr = None # OK
    dpvat:              typing.AnyStr = None # OK
    taxa_licenciamento: typing.AnyStr = None # OK

    data: typing.List[dict] = dataclasses.field(default_factory=list)

    multas: Multas = None

    def __post_init__(self):

        self.is_valid = self.has_elmt(By.ID, "tituloPaginaPlaceHolder_txtDataConsulta")

        if self.is_valid:
            self.placa = self.grab_text(By.ID, "conteudoPaginaPlaceHolder_txtPlaca")
            self.renavam = self.grab_text(By.ID, "conteudoPaginaPlaceHolder_txtRenavam")
            self.dpvat = self.grab_text(By.XPATH, '/html/body/form/table[3]/tbody/tr/td[2]/table/tbody/tr/td[2]/div/table[22]/tbody/tr/td/table/tbody/tr[2]/td[5]', default=0.00)

            # = Ipva ===
            ipva = \
                Ipva(self.driver)

            self.ipva = ipva.ipva

            # = Licenciamento ===
            licenciamento = \
                Licenciamento(self.driver)

            self.taxa_licenciamento = licenciamento.total_licenciamento

            # = Multas ===
            self.multas = \
                MultasDetalhadas(self.driver)
            
            self.multas_detran = self.multas.detran
            self.outras_multas_sp = self.multas.outras_multas
            self.multas_renainf = self.multas.renainf

            # = Divida ativa ===
            divida_ativa = \
                DividaAtiva(self.driver, self.renavam, anti_captcha_key=self.anti_captcha_key)
            
            self.divida_ativa = divida_ativa.total

            self.process_debt()

    def process_debt(self) -> typing.NoReturn:
        order = [
            # { 'name' : 'outras_multas', 'value' : self.outras_multas_sp },
            { 'name' : 'ipva', 'value' : self.ipva },
            { 'name' : 'divida_ativa', 'value' : self.divida_ativa },

            { 'name' : 'multas_detran', 'value' : self.multas_detran },
            { 'name' : 'renainf', 'value' : self.multas_renainf },
            { 'name' : 'outras_multas', 'value' : self.outras_multas_sp },
            { 'name' : 'taxa_licenciamento', 'value' : self.taxa_licenciamento },
        ]


        for index, seq in enumerate(order):
            ait = "RENAVAM"
            guia = "RENAVAM"
            pay_type = seq['name'].upper()


            # se a divida estiver zerada pula o mesmo
            if seq['value'] <= 0:
                continue    

            if (self.balance - seq['value']) < 0:
                
                # Paga tudo ou nada
                if seq['name'] in ('renainf', 'ipva', 'taxa_licenciamento'):
                    break
                
                elif seq['name'] in ('divida_ativa'):
                    
                    # subtrai o saldo
                    self.balance -= seq['value']
                    pay_type = "DIVIDA ATIVA"

                    # Paga com total ou parcial
                    seq['value'] += self.balance

                    # break

                elif(seq['name'] == "multas_detran" and seq['value'] > self.balance):

                    detran = selecionar_contas(self.balance, \
                        list(filter(lambda x: x['name']=="DETRAN", self.multas.detalhamento))
                    )
                    
                    for d in detran:
                        self.balance -= d['value']

                        # self.data.append([
                        #     self.lote,
                        #     self.placa,
                        #     self.renavam,
                        #     d['value'],
                        #     d['ait'],
                        #     d['guia'],
                        #     "MULTA DETRAN",
                        # ])

                        self.data.append({
                            "lote": self.lote,
                            "placa": self.placa,
                            "renavam": self.renavam,
                            "valor": d['value'],
                            "ait": d['ait'],
                            "guia": d['guia'],
                            "tipo_debito": "MULTA DETRAN",
                        })
                        


                    # break

                elif(seq['name'] == "outras_multas" and seq['value'] > self.balance):

                    der = selecionar_contas(self.balance, \
                        list(filter(lambda x: x['name']=="D.E.R.", self.multas.detalhamento))
                    )

                    for d in der:
                        self.balance -= d['value']

                        # self.data.append([
                        #     self.lote,
                        #     self.placa,
                        #     self.renavam,
                        #     d['value'],
                        #     d['ait'],
                        #     d['guia'],
                        #     "D.E.R.",
                        # ])

                        
                        self.data.append({
                            "lote": self.lote,
                            "placa": self.placa,
                            "renavam": self.renavam,
                            "valor": d['value'],
                            "ait": d['ait'],
                            "guia": d['guia'],
                            "tipo_debito": "D.E.R.",
                        })

                    municipal = selecionar_contas(self.balance, \
                        list(filter(lambda x: x['name']=="MUNICIPAL", self.multas.detalhamento))
                    )
                        
                    for m in municipal:
                        self.balance -= m['value']

                        # self.data.append([
                        #     self.lote,
                        #     self.placa,
                        #     self.renavam,
                        #     m['value'],
                        #     m['ait'],
                        #     m['guia'],
                        #     "MUNICIPAL",
                        # ])

                        self.data.append({
                            "lote": self.lote,
                            "placa": self.placa,
                            "renavam": self.renavam,
                            "valor": m['value'],
                            "ait": m['ait'],
                            "guia": m['guia'],
                            "tipo_debito": "MUNICIPAL",
                        })

                        

                    convenio = selecionar_contas(self.balance, \
                        list(filter(lambda x: x['name']=="CONVENIO", self.multas.detalhamento))
                    )

                    for c in convenio:
                        self.balance -= c['value']

                        # self.data.append([
                        #     self.lote,
                        #     self.placa,
                        #     self.renavam,
                        #     c['value'],
                        #     c['ait'],
                        #     c['guia'],
                        #     "CONVENIO",
                        # ])

                        self.data.append({
                            "lote": self.lote,
                            "placa": self.placa,
                            "renavam": self.renavam,
                            "valor": c['value'],
                            "ait": c['ait'],
                            "guia": c['guia'],
                            "tipo_debito": "CONVENIO",
                        })
                  


                    # break

                # caso nao tenha saldo pula a sequencia
                if not seq['name'] in ('divida_ativa'):
                    # self.data.append([
                    #     self.lote,
                    #     self.placa,
                    #     self.renavam,
                    #     '-',
                    #     '-',
                    #     '-',
                    #     '-1',
                    # ])

                    self.data.append({
                        "lote": self.lote,
                        "placa": self.placa,
                        "renavam": self.renavam,
                        "valor": '0.00',
                        "ait": '-',
                        "guia": '-',
                        "tipo_debito": '-1',
                    })
                    continue
            else:
                self.balance-=seq['value']

            # renomeando
            if seq['name'] == 'divida_ativa':
                ait = "BOLETO"
                guia = "BOLETO"

            elif seq['name'] == 'multas_detran':
                pay_type = "MULTA DETRAN (PAGAR TUDO)"

            elif seq['name'] == 'outras_multas':
                pay_type = "OUTRAS MULTAS SP (PAGAR TUDO)"
            
            elif seq['name'] == 'taxa_licenciamento':
                pay_type = "TAXA DE LICENCIAMENTO"

            # self.data.append([
            #     self.lote,
            #     self.placa,
            #     self.renavam,
            #     seq['value'],
            #     ait,
            #     guia,
            #     pay_type,
            # ])

            self.data.append({
                "lote": self.lote,
                "placa": self.placa,
                "renavam": self.renavam,
                "valor": seq['value'],
                "ait": ait,
                "guia": guia,
                "tipo_debito": pay_type,
            })
    
    def __iter__(self) -> typing.List:
        
        return iter(self.data)

@dataclasses.dataclass
class SFP(GrabOnPage):
    anti_captcha_key: str

    is_valid: bool = False

    renavam:            typing.AnyStr = None # OK
    placa:              typing.AnyStr = None # Ok
    ipva:               typing.AnyStr = None # OK
    divida_ativa:       typing.AnyStr = None # OK
    multas_renainf:     typing.AnyStr = None # OK
    multas_detran:      typing.AnyStr = None # Ok
    outras_multas_sp:   typing.AnyStr = None # OK
    dpvat:              typing.AnyStr = None # OK
    taxa_licenciamento: typing.AnyStr = None # OK


    def __post_init__(self):

        self.is_valid = self.has_elmt(By.ID, "tituloPaginaPlaceHolder_txtDataConsulta")

        if self.is_valid:
            self.placa = self.grab_text(By.ID, "conteudoPaginaPlaceHolder_txtPlaca")
            self.renavam = self.grab_text(By.ID, "conteudoPaginaPlaceHolder_txtRenavam")
            self.dpvat = self.grab_text(By.XPATH, '/html/body/form/table[3]/tbody/tr/td[2]/table/tbody/tr/td[2]/div/table[22]/tbody/tr/td/table/tbody/tr[2]/td[5]', default=0.00)

            # = Ipva ===
            ipva = \
                Ipva(self.driver)

            self.ipva = ipva.ipva

            # = Multas ===
            multas = \
                Multas(self.driver)
            
            self.multas_detran = multas.detran
            self.outras_multas_sp = multas.outras_multas
            self.multas_renainf = multas.renainf

            # = Licenciamento ===
            licenciamento = \
                Licenciamento(self.driver)

            self.taxa_licenciamento = licenciamento.total_licenciamento

            # = Divida ativa ===
            divida_ativa = \
                DividaAtiva(self.driver, self.renavam, anti_captcha_key=self.anti_captcha_key)
            
            self.divida_ativa = divida_ativa.total

@dataclasses.dataclass
class DividaAtiva(GrabOnPage):
    renavam: typing.AnyStr
    anti_captcha_key: typing.AnyStr

    is_valid: bool = False
    total: float = dataclasses.field(default_factory=float)

    def __post_init__(self):

        ignore_divida_ativa = False
        key = self.anti_captcha_key

        if "NADA CONSTA" not in self.grab_text(By.ID, "conteudoPaginaPlaceHolder_txtExisteDividaAtiva"):

            if not ignore_divida_ativa:
                self.driver.get("https://www.dividaativa.pge.sp.gov.br/sc/pages/consultas/consultarDebito.jsf")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "consultaDebitoForm:consulta"))
                )
                self.is_valid = self.has_elmt(By.ID, "consultaDebitoForm:consulta")
            
            else:
                self.total = "COM"

        if self.is_valid:

            
            
            # ------ Codigo feio
            
            sl = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa"))
                )
            
            sl = Select(sl)

            # sl = Select(self.driver.find_element(By.ID,"consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa"))
            sl.select_by_value('RENAVAM')
            
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "consultaDebitoForm:decTxtTipoConsulta:cdaEtiqueta"))
            )
            
            element.send_keys(self.renavam)
            
            
            for i in range(1):
                if ReCaptcha(self.driver, key, recaptcha_data_site_key_ID="recaptcha").solve(recaptcha_res="g-recaptcha-response"):
                    break
                    
        

            self.driver.find_element(By.NAME, "consultaDebitoForm:j_id104").click()
            
            # ------- fim de codigo feio
            
            
            sl = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa"))
            )
            
            
            # sl = Select(sl)
            # sl.select_by_value('RENAVAM')
            
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "consultaDebitoForm:decTxtTipoConsulta:renavam"))
            )

            element.send_keys(self.renavam)
            
            for i in range(1):
                if ReCaptcha(self.driver, key, recaptcha_data_site_key_ID="recaptcha").solve(recaptcha_res="g-recaptcha-response"):
                    break
                                   
            self.driver.find_element(By.NAME, "consultaDebitoForm:j_id104").click()

            if self.has_elmt(By.ID, "consultaDebitoForm:dataTable:j_id164"):
                _ = self.grab_text(By.ID, "consultaDebitoForm:dataTable:j_id164")

                self.total = custom_to_float(_)
