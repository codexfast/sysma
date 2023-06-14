import time

from models.sys import GeneralSettings
from sqlalchemy.orm import Session
from config import DB_ENGINE

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows



def _delay(delay:int = 2) -> int:
    time.sleep(delay)

    return delay

def create_webdriver() -> webdriver.Chrome:
    headless_window = True

    with Session(DB_ENGINE) as session:

        general:GeneralSettings = session.query(GeneralSettings).one_or_none()

        if general:
            headless_window = general.headless_mode


    # headless_window = bool(int(os.getenv("HEADLESS_WINDOW", False)))

    # Baixa driver # Disable
    # chrome_driver = Service(ChromeDriverManager().install())
    chrome_driver = Service(executable_path="assets/webdriver/chromedriver.exe")

    chrome_driver.creation_flags = CREATE_NO_WINDOW
    
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1024,768");
    options.add_argument("--no-sandbox");

    if headless_window:
        options.add_argument("--headless");

    options.add_argument("--disable-gpu");
    options.add_argument("--disable-crash-reporter");
    options.add_argument("--disable-extensions");
    options.add_argument("--disable-in-process-stack-traces");
    options.add_argument("--disable-logging");
    options.add_argument("--disable-dev-shm-usage");
    options.add_argument("--log-level=3");
    options.add_argument("--output=/dev/null");

    driver = webdriver.Chrome(options=options, service=chrome_driver)
    # driver = webdriver.Chrome(options=options, executable_path="assets/webdriver/chromedriver.exe")

    if headless_window:
        driver.minimize_window()

    return driver