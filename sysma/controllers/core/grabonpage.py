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
                self.is_valid = self.has_elmt(By.ID, "consultaDebitoForm:consulta")
            
            else:
                self.total = "COM"

        if self.is_valid:
            
            # ------ Codigo feio
            
            sl = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa"))
                )
            
            sl = Select(sl)

            # sl = Select(self.driver.find_element(By.ID,"consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa"))
            sl.select_by_value('RENAVAM')
            
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "consultaDebitoForm:decTxtTipoConsulta:cdaEtiqueta"))
            )
            
            element.send_keys(self.renavam)
            
            
            for i in range(1):
                if ReCaptcha(self.driver, key, recaptcha_data_site_key_ID="recaptcha").solve(recaptcha_res="g-recaptcha-response"):
                    break
                    
        

            self.driver.find_element(By.NAME, "consultaDebitoForm:j_id102").click()
            
            # ------- fim de codigo feio
            
            
            """sl = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa"))
            )
            """
            
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
