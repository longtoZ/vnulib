from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

class Utils:
    def __init__(self, webdriver: WebDriver):
        self.webdriver = webdriver

    def waitUntilVisible(self, selector: str, timeout: int):
        return WebDriverWait(self.webdriver, timeout).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def waitUntilClickable(self, selector: str, timeout: int):
        return WebDriverWait(self.webdriver, timeout).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def waitUntilUrlChanged(self, url: str, timeout: int):
        WebDriverWait(self.webdriver, timeout).until(ec.url_changes(url))
