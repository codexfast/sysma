"""
Solve google recaptcha
"""
import dataclasses
import typing

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

@dataclasses.dataclass
class ReCaptcha:
    driver: webdriver.Chrome
    solver_key: typing.AnyStr
    recaptcha_data_site_key_ID: typing.AnyStr = dataclasses.field(default="conteudoPaginaPlaceHolder_g_recaptcha")
    recaptcha_key: typing.AnyStr = dataclasses.field(init=False)
    solver: recaptchaV2Proxyless = dataclasses.field(init=False)

    def __post_init__(self):
        try:
            self.recaptcha_key = self.driver.find_element(
                By.ID, 
                self.recaptcha_data_site_key_ID
            ).get_attribute('data-sitekey')

            self.solver = recaptchaV2Proxyless()

            # Imprime logs
            # self.solver.set_verbose(1)
            self.solver.set_key(self.solver_key)

        except NoSuchElementException as err:
            raise NoSuchElementException("Iframe reCaptcha não encontrado!")
        
        # except

    def __repr__(self) -> str:
        return f'{self.recaptcha_key}'

    def solve(self, recaptcha_res: str) -> bool:
        try:

            self.solver.set_website_url(self.driver.current_url)
            self.solver.set_website_key(self.recaptcha_key)

            response = self.solver.solve_and_return_solution()
            

            if response:
                self.driver.execute_script(
                    f"document.getElementById('{recaptcha_res}').innerHTML = '{response}'"
                )

                return True
        except NoSuchElementException as err:
            print(err)

        return False
