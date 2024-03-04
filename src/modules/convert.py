import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import img2pdf
import PyPDF2
from ..CONSTANTS import *

class Convert:
    def __init__(self, departure: str, destination: str, title: str, fast: bool, merge: bool):
        self.departure = departure
        self.destination = destination
        self.sections = sorted(os.listdir(self.departure), key=lambda section: int(section.split("section")[1]))
        self.title = title
        self.fast = fast
        self.merge = merge

    # Convert images in one section to PDF
    def singleConvert(self, section: str, order: int):
        imgs = []

        for f in os.listdir(os.path.join(self.departure, section)):
            if f.endswith(".jpg"):
                imgs.append(os.path.join(self.departure, section, f))

        imgs.sort(key=lambda image: int(image.split("page")[1].split(".")[0]))

        with open(f"{self.destination}{self.title}_section{order}.pdf", "wb") as f:
            f.write(img2pdf.convert(imgs))
            f.close()


    def convert(self):
        print(f"{GREEN}[+] Converting...{RESET}")

        # If fast mode is enabled, use multithreading
        if (self.fast):
            with ThreadPoolExecutor(max_workers=len(self.sections)) as executor:
                futures = []

                for order, section in enumerate(self.sections):
                    future = executor.submit(self.singleConvert, section, order)
                    futures.append(future)

                for future in as_completed(futures):
                    future.result()

                executor.shutdown()
        
        # Otherwise, use single thread
        else:
            for order, section in enumerate(self.sections):
                self.singleConvert(section, order)

        # Merge the PDFs
        if self.merge:
            pdfs = [file for file in os.listdir(self.destination) if file.endswith(".pdf")]
            pdfs.sort(key=lambda pdf: int(pdf.split("section")[1].split(".")[0]))

            pdf_merger = PyPDF2.PdfMerger()

            with open(f"{self.destination}{self.title}.pdf", "wb") as f:

                for pdf in pdfs:
                    pdf_merger.append(f"{self.destination}{pdf}")
                
                pdf_merger.write(f)
                pdf_merger.close()
                f.close()
            
            for pdf in pdfs:
                os.remove(f"{self.destination}{pdf}")

        print(f"{GREEN}[+] Converted successfully.{RESET}")
