import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException
from .update_driver import UpdateDriver
from ..CONSTANTS import *

class Browser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.updateDriver = UpdateDriver()

    def browserSetup(self):
        self.options.add_argument("--log-level=2")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_experimental_option("detach", True)

        try:
            if not (os.path.exists("chromedriver.exe")):
                print(f"{RED}[!] Driver not found. Installing...{RESET}")
                self.updateDriver.update()

            service = Service()
            driver = webdriver.Chrome(options=self.options, service=service)

        except SessionNotCreatedException:
            print(f"{YELLOW}[-] Driver is out-of-date. Updating...{RESET}")
            self.updateDriver.update()
            service = Service()
            driver = webdriver.Chrome(options=self.options, service=service)

        return driver
