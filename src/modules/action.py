import os
import shutil
from tqdm import tqdm
from urllib.parse import urlparse, parse_qs
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from .utils import Utils
from ..CONSTANTS import *


class Actions:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.utils = Utils(driver)
        self.skip = False

    # Gather all sections' links
    def gatherLinks(self, url: str):
        if "https://ir.vnulib.edu.vn/handle/" not in url:
            print(f"{RED}[!] Invalid URL.{RESET}")
            self.skip = True
            return

        print(f"\nStarting action: {GREEN}{url}{RESET}")
        
        self.driver.get(url)
        summary = self.utils.waitUntilVisible(".item-summary-view-metadata", 10)
        title = self.utils.waitUntilVisible('h2[class="ds-div-head"]', 10).text.strip()

        links = [
            i.get_attribute("href")
            for i in summary.find_elements(By.CSS_SELECTOR, ".pdf-view.viewonline")
        ]

        print(f"{GREEN}[+] Found {len(links)} sections {RESET}")

        if len(links) == 0:
            print(f"{RED}[!] No sections found. Skipping current url...{RESET}")
            self.skip = True
            return

        return {
            "title": title,
            "links": links,
        }

    # Get pages info (doc, subfolder, total page) for each section
    def gatherImagesRange(self, links: str):
        data = []

        with tqdm(total=len(links), desc="[+] Gathering all pages info") as pbar:
            for link in links:
                self.driver.get(link)

                self.utils.waitUntilVisible("#pageContainer_0_documentViewer_textLayer", 10)

                totalPage = self.utils.waitUntilVisible(".flowpaper_lblTotalPages", 10)
                totalPage = int(totalPage.text.strip().replace(" ", "").replace("/", ""))

                parsedUrl = urlparse(self.driver.current_url)
                docValue = parse_qs(parsedUrl.query)["doc"][0]
                subfolderValue = parse_qs(parsedUrl.query)["subfolder"][0]

                data.append(
                    {"doc": docValue, "subfolder": subfolderValue, "page": totalPage}
                )
                pbar.update(1)

        print(f"{GREEN}[+] All pages info gathered {RESET}")
        return data

    # Remove all images in directory
    def cleanUp(self, path: str):
        if os.path.exists(path):
            print(f"{YELLOW}[-] Cleaning up...{RESET}")
            shutil.rmtree(path, ignore_errors=True)
        else:
            print(
                f"{YELLOW}[-] Departure folder does not exist. Nothing to clean up.{RESET}"
            )
