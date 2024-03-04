from datetime import datetime
from src import Parse, Browser, Login, Actions, MultiThreadingDownload, Convert


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
        MultiThreadingDownload(sections, departure, destination, fast).createTasks()
        Convert(departure, destination, title, fast, merge).convert()

        if clean:
            action.cleanUp(departure)


def main():
    parsed = Parse().parse()
    work(parsed["url"], parsed["fast"], parsed["merge"], parsed["clean"])


if __name__ == "__main__":
    main()
