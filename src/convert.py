import img2pdf
import os
from .CONSTANTS import *


class Convert:
    def __init__(self):
        return

    def convert(self, departure, destination):
        imgs = []

        for f in os.listdir(departure):
            if f.endswith(".jpg"):
                imgs.append(os.path.join(departure, f))

        sorted_imgs = sorted(
            imgs, key=lambda image: int(image.split("page")[1].split(".")[0])
        )

        # with PixelSpinner('[+] Converting...') as bar:
        print(f"{GREEN}[+] Converting...{RESET}")

        with open(f"{destination}Book.pdf", "wb") as f:
            f.write(img2pdf.convert(sorted_imgs))
            f.close()

        print(f"{GREEN}[+] Converted successfully.{RESET}")
