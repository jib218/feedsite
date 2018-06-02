from .models import Item

from bs4 import BeautifulSoup


def clean_description(i: Item):
    if i.description is None:
        return
    soup = BeautifulSoup(i.description, "html.parser")

    for img in soup.find_all("img"):
        img.decompose()

    for link in soup.find_all("a"):
        link["target"] = "_blank"
        link["rel"] = "noreferrer"

    i.description = soup.prettify()
