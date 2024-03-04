import os
import json

from .browser import Browser
from .utils import Utils
from ..CONSTANTS import *

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec


class Login:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.driver = self.browser.browserSetup()
        self.utils = Utils(self.driver)
        self.username = ""
        self.password = ""

    def checkAuthorizationFile(self):
        if not os.path.exists("authorization.json"):
            print('here')
            with open("authorization.json", "w") as f:
                json.dump({"username": "", "password": ""}, f)
                f.close()
            
            print(f"{YELLOW}[+] authorization.json not found, created one. Please provide your credentials before starting the program.{RESET}")
            return False
        else:
            with open("authorization.json", "r") as f:
                data = json.load(f)
                self.username = data["username"]
                self.password = data["password"]
                f.close()
            return True

    def missingCredentials(self):
        if self.username == "" or self.password == "":
            return True
        return False

    def login(self) -> WebDriver:
        if self.checkAuthorizationFile():
            if self.missingCredentials():
                print(
                    f"{RED}[!] Please provide your credentials before starting the program.{RESET}"
                )
                raise SystemExit
        else:
            raise SystemExit
            

        print(f"Logging in...")
        self.driver.get("https://ir.vnulib.edu.vn/login/oa/dologin.jsp?RedirectURL=/")

        usernameInput = self.utils.waitUntilVisible(
            '.form-control[name="username"]', 10
        )
        passwordInput = self.utils.waitUntilVisible(
            '.form-control[name="password"]', 10
        )

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)

        loginButton = self.utils.waitUntilClickable('button[type="submit"]', 10)
        loginButton.click()

        if "https://ir.vnulib.edu.vn/" in self.driver.current_url:
            print(f"{GREEN}[+] Login successfully.{RESET}")

            return self.driver

        else:
            print(f"{RED}[!] Login failed.{RESET}")
            return
