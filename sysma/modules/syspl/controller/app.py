from collections.abc import Callable, Iterable, Mapping
from controller.core.web import create_webdriver
from controller.core.web import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tkinter.messagebox import showerror

import customtkinter
import threading

class Syspl(threading.Thread):

    def __init__(
            self,
            threadId: int,
            threadName: str,
            view: customtkinter.CTk,
            pb_step: customtkinter.CTkProgressBar, 
            lb_step: customtkinter.CTkLabel, 
            lb_perc: customtkinter.CTkLabel,
        ):

        threading.Thread.__init__(self)

        self.view = view
        self.threadId = threadId
        self.threadName = threadName
        self.pb_step = pb_step
        self.lb_step = lb_step
        self.lb_perc = lb_perc

        self.driver: webdriver = create_webdriver()

    def run(self):
        car = 788
        iter_ = 1/car

        # self.pb_step.start()
        self.pb_step.set(0)

        self.do_login()

        for c in range(1,car):

            self.view.update()

            try:
                self.pb_step.set(c*(iter_))
                
            except:
                self.driver.close()
                break



    def do_login(self):
        self.driver.get("https://www.sispl.sp.gov.br/maximo/webclient/login/login.jsp")

        # Encontra input usuario e preenche com login
        username = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        username.send_keys("36490625857")

        # Encontra input senha e preenche com senha
        password = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys("rennan10")

        # envia input
        clickable = self.driver.find_element(By.XPATH, '//*[@id="loginbutton"]')
        clickable.click()


        try:
            # SE NAO ENCONTRAR JA SABE NÉ BOY
            self.driver.find_element(By.ID, "titlebar-tb_appname")

        except NoSuchElementException:
            showerror("Login", "Não foi possível logar")

            return False

        return self.driver.current_url
