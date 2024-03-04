from ..CONSTANTS import *


class Parse:
    def __init__(self):
        pass

    def parse(self):
        parser = {"url": [], "fast": False, "merge": False, "clean": False}

        parser["url"] = list(
            input("[+] Enter the URL(s) of the book(s) (separated by space): ").split(
                " "
            )
        )

        fast = input("[+] Fast mode? (y/n): ").strip().lower()

        if fast == "y" or fast == "":
            parser["fast"] = True

        merge = input("[+] Merge sections? (y/n): ").strip().lower()

        if merge == "y" or merge == "":
            parser["merge"] = True

        clean = (
            input("[+] Clean up the downloaded images after converting to PDF? (y/n): ")
            .strip()
            .lower()
        )

        if clean == "y" or clean == "":
            parser["clean"] = True

        print(
            f"\n[+] URL(s): {GREEN}{' '.join(parser['url'])}{RESET} \n[+] Fast mode: {GREEN}{parser['fast']}{RESET} \n[+] Merge sections: {GREEN}{parser['merge']}{RESET} \n[+] Clean up: {GREEN}{parser['clean']}{RESET}\n"
        )

        return parser
