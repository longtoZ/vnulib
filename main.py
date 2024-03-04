from datetime import datetime
from src import Parse, Browser, Login, Actions, Download, Convert

def work(urls: list, fast: bool, merge: bool, clean: bool):
    browser = Browser()
    login = Login(browser)

    driver = login.login()

    for bookUrl in urls:
        directory_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        departure = f"imgs/{directory_name}/"
        destination = f"pdfs/{directory_name}/"

        action = Actions(driver)

        summary = action.gatherLinks(bookUrl)

        if action.skip:
            continue

        links = summary["links"]
        title = summary["title"]

        sections = action.gatherImagesRange(links)
        Download(sections, departure, destination, fast).createTasks()
        Convert(departure, destination, title, fast, merge).convert()

        if clean:
            action.cleanUp(departure)

def main():
    parsed = Parse().parse()

    # Start timer
    start = datetime.now()

    work(parsed["url"], parsed["fast"], parsed["merge"], parsed["clean"])
    
    end = datetime.now()
    seconds = (end - start).seconds
    total = lambda seconds: f"{(seconds//60):02d}:{(seconds%60):02d}" 
    print(f"[+] Total time: {total(seconds)}")

if __name__ == "__main__":
    main()