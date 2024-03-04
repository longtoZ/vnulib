import os
import shutil
import wget
import zipfile
import requests
from bs4 import BeautifulSoup


class UpdateDriver:
    def __init__(self):
        pass

    def update(self):
        url = ""
        pageUrl = "https://googlechromelabs.github.io/chrome-for-testing/"
        page = requests.get(pageUrl)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")

            tr = soup.select("#stable tbody tr")

            for i in tr:
                if (
                    i.find_all("th")[1].find("code").text == "win64"
                    and i.find_all("th")[0].find("code").text == "chromedriver"
                ):
                    url = i.find_all("td")[0].find("code").text
                    break

        latestDriverZip = wget.download(url, "chromedriver.zip")

        with zipfile.ZipFile(latestDriverZip, "r") as zip_ref:
            zip_ref.extractall()
            zip_ref.close()

        os.remove(latestDriverZip)
        shutil.move("chromedriver-win64/chromedriver.exe", "chromedriver.exe")
        shutil.rmtree("chromedriver-win64")
