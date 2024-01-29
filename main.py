from datetime import datetime
from src import Browser, Login, Actions, Convert


def parse():
    parser = {"url": [], "clean": False}

    parser["url"] = list(
        input("[+] Enter the URL(s) of the book(s) (separated by space): ").split(" ")
    )
    clean = (
        input("[+] Clean up the downloaded images after converting to PDF? (y/n): ")
        .strip()
        .lower()
    )

    if clean == "y" or clean == "":
        parser["clean"] = True

    return parser


def work(urls: list, clean: bool):
    browser = Browser()
    login = Login(browser)

    driver = login.login()

    for bookUrl in urls:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        departure = f"imgs/{filename}/"
        destination = f"pdfs/{filename}/"

        action = Actions(driver)

        links = action.gatherLinks(bookUrl)
        if action.skip:
            continue

        ranges = action.gatherImagesRange(links)
        action.downloadImages(ranges, departure, destination)
        Convert().convert(departure, destination)

        if clean:
            action.cleanUp(departure)


def main():
    parsed = parse()
    work(parsed["url"], parsed["clean"])


if __name__ == "__main__":
    main()
