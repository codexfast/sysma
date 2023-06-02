import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def _delay(delay:int = 2) -> int:
    time.sleep(delay)

    return delay

def create_webdriver() -> webdriver.Chrome:

    headless_window = True
    # headless_window = bool(int(os.getenv("HEADLESS_WINDOW", False)))

    # Baixa driver
    chrome_driver = Service(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", False)
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

    driver = webdriver.Chrome(service=chrome_driver, options=options)

    if headless_window:
        driver.minimize_window()

    return driver