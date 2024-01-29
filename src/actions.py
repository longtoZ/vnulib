import os
import shutil
import requests
from progress.bar import Bar
from urllib.parse import urlparse, parse_qs
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from .utils import Utils
from .CONSTANTS import *


class Actions:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.utils = Utils(driver)
        self.skip = False

    def gatherLinks(self, url: str):
        if "https://ir.vnulib.edu.vn/handle/" not in url:
            print(f"{RED}[!] Invalid URL.{RESET}")
            self.skip = True
            return

        print(f"\nStarting action: {GREEN}{url}{RESET}")
        self.driver.get(url)
        summary = self.utils.waitUntilVisible(".item-summary-view-metadata", 10)

        links = [
            i.get_attribute("href")
            for i in summary.find_elements(By.CSS_SELECTOR, ".pdf-view.viewonline")
        ]

        print(f"{GREEN}[+] Found {len(links)} links {RESET}")

        if len(links) == 0:
            print(f"{RED}[!] No links found. Skipping current url...{RESET}")
            self.skip = True
            return

        return links

    def gatherImagesRange(self, links: str):
        print(f"[+] Gathering all pages info...")
        data = []

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

        print(f"{GREEN}[+] All pages info gathered {RESET}")
        return data

    def downloadImages(self, data: list, departure: str, destination: str):
        if not os.path.exists(departure):
            print(
                f"{YELLOW}[-] Departure folder does not exist. Creating one...{RESET}"
            )
            os.makedirs(departure)

        if not os.path.exists(destination):
            print(
                f"{YELLOW}[-] Destination folder does not exist. Creating one...{RESET}"
            )
            os.makedirs(destination)

        countPage = 1

        for i in data:
            with Bar(
                "[+] Downloading images", fill="-", suffix="%(percent).1f%% - %(eta)ds"
            ) as bar:
                for page in range(1, i["page"] + 1):
                    pattern = f'https://ir.vnulib.edu.vn/flowpaper/services/view.php?doc={i["doc"]}&format=jpg&page={page}&subfolder={i["subfolder"]}'
                    img = requests.get(pattern, verify=False).content
                    f = open(f"{departure}page{countPage}.jpg", "wb")
                    f.write(img)
                    f.close()
                    countPage += 1
                    bar.next()

    def cleanUp(self, path: str):
        if os.path.exists(path):
            print(f"{YELLOW}[-] Cleaning up...{RESET}")
            shutil.rmtree(path, ignore_errors=True)
        else:
            print(
                f"{YELLOW}[-] Departure folder does not exist. Nothing to clean up.{RESET}"
            )
