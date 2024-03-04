from concurrent.futures import ThreadPoolExecutor, as_completed
import os 
import requests
import math 
from tqdm import tqdm
from ..CONSTANTS import *

class MultiThreadingDownload:
    def __init__(self, sections: list, departure: str, destination: str, fast: bool):
        self.factor = 50
        self.page_limit = 150

        self.sections = sections
        self.total_pages = sum([section["page"] for section in sections])
        self.departure = departure
        self.destination = destination
        self.fast = fast
        self.workers = math.floor(self.total_pages/self.factor) if (self.total_pages > self.page_limit and len(self.sections) == 1) else len(self.sections)
    
    def downloadImages(self, data: dict, order: int, start_page: int, end_page: int, pbar: tqdm):
        section = f"{self.departure}section{order}/"

        if not os.path.exists(section):
            os.makedirs(section)

        for page in range(start_page, end_page + 1):
            pattern = f'https://ir.vnulib.edu.vn/flowpaper/services/view.php?doc={data["doc"]}&format=jpg&page={page}&subfolder={data["subfolder"]}'
            
            # Handle image timeout exception
            try:
                img = requests.get(pattern, verify=False, timeout=10).content
                f = open(f"{section}page{start_page}.jpg", "wb")
                f.write(img)
                f.close()
            except requests.exceptions.RequestException:
                img = open("src/img/blank.jpg", "rb").read()
                f = open(f"{section}error_page{start_page}.jpg", "wb")
                f.write(img)
                f.close()

            start_page += 1

            # Update progress bar in percentage
            with pbar.get_lock():
                pbar.update(1)

    def createTasks(self):        
        if not os.path.exists(self.departure):
            print(
                f"{YELLOW}[-] Departure folder does not exist. Creating one...{RESET}"
            )
            os.makedirs(self.departure)

        if not os.path.exists(self.destination):
            print(
                f"{YELLOW}[-] Destination folder does not exist. Creating one...{RESET}"
            )
            os.makedirs(self.destination)

        # Generate progress bar
        with tqdm(total=self.total_pages, desc="Downloading images") as pbar:
            
            # If fast mode is enabled, use multithreading
            if (self.fast):
                # Create a thread pool with the number of workers based on the number of sections
                with ThreadPoolExecutor(max_workers=self.workers) as executor:
                    futures = []

                    # If the total pages is greater than 100 and there is only one section, divide the pages into chunks
                    if (self.total_pages > 100 and len(self.sections) == 1):
                        data = self.sections[0]

                        for order in range(self.workers+1):
                            start_page = 1 + (order * self.factor)
                            end_page = start_page + self.factor - 1 if start_page + self.factor - 1 <= data["page"] else data["page"]

                            future = executor.submit(self.downloadImages, data, order, start_page, end_page, pbar)
                            futures.append(future)

                    # Otherwise, download the images as usual
                    else:
                        for order, data in enumerate(self.sections):
                            start_page = 1
                            end_page = data["page"]

                            future = executor.submit(self.downloadImages, data, order, start_page, end_page, pbar)
                            futures.append(future)

                    for future in as_completed(futures):
                        future.result()

                    executor.shutdown()
            
            # Otherwise, use single thread
            else:
                for order, data in enumerate(self.sections):
                    start_page = 1
                    end_page = data["page"]
                
                    self.downloadImages(data, order, start_page, end_page, pbar)
