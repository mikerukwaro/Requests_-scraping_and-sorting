from bs4 import BeautifulSoup
import requests
import re

search_term = input("what do you want to search: ")

url = "https://www.newegg.com/p/pl?d=3080&n=8000"
response = requests.get(url).text
soup = BeautifulSoup(response, "html.parser")

pages = soup.find(class_="list-tool-pagination-text").strong
pages_split = int(str(pages).split("/")[1].split(">")[-1].split("<")[0])
items_found = {}
for page in range(1, pages_split + 1):
    url = f"https://www.newegg.com/p/pl?d=3080&n=8000&page={page}"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    div = soup.find(
        class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell"
    )
    items = div.find_all(text=re.compile(search_term))

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue

        link = parent["href"]
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", " ")), "link": link}

        except:
            pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])
for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]["link"])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")