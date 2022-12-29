from bs4 import BeautifulSoup
import pandas as pd
# Path: main.py
import time
from selenium import webdriver

browser = webdriver.Chrome()

import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
}
url = "https://www.newegg.com/"

browser.get(url)
time.sleep(14)
soup = BeautifulSoup(browser.page_source, 'lxml')



menu = soup.find("div", {"class": "menu-body"})


urls = menu.find_all("li", {"class" : "menu-level-3 menu at-right"})
i = 1

data = []
for url in urls:
    i+=1
    link = url.find("a", {"class": "menu-list-link bg-transparent-lightblue"})
    txt_menu = requests.get(link["href"], headers = headers)
    menu_soup = BeautifulSoup(txt_menu.text, "lxml")
    title = menu_soup.find("div", {"class": "dynamic-module-title"})
    link_in = title.find("a")

    txt_option = requests.get(link_in["href"], headers = headers)
    option_soup = BeautifulSoup(txt_option.text, "lxml")

    item = option_soup.find("div", {"class": "dynamic-module-title"})
    item_link = item.find("a")

    txt_choice = requests.get(item_link["href"], headers = headers)
    choice_soup = BeautifulSoup(txt_choice.text, "lxml")

    products = choice_soup.find("div", {"class": "item-cell"})
    last_page = choice_soup.find_all("div", {"class": "btn-group-cell"})
    number = int(last_page[-2].text)
    new = products.find("a")
    i = 2
    while True:
        new_txt = requests.get(f"https://www.newegg.com/p/pl?N=100007671%20601306860&page={i}", headers = headers)
        new_page = BeautifulSoup(new_txt.text, "lxml")
        prods = new_page.find_all("div", {"class": "item-cell"})
        for prod in prods:
            info = prod.find("a")
            product_text = requests.get(info["href"], headers = headers)
            product_info = BeautifulSoup(product_text.text, "lxml")
            title = product_info.find("h1", {"class": "product-title"})
            description = product_info.find("div", {"class": "product-bullets"})
            list = description.find("ul" , recursive=False)

            seller_info = product_info.find("div", {"class": "product-seller"})

            seller = seller_info.find("a")
            price = product_info.find("li", {"class": "price-current"})
            main_picture = product_info.find("img", {"id": "mainSlide9SIAP08GPR6677"})

            rating = product_info.find("i", {"class": "rating rating-4"})
            list_items = list.find_all("li" , recursive=False)
            string = ""
            for item in list_items:
                string += item.text + "\n"
            
            data.append([title.text, string, price.text, rating["title"], seller["title"], main_picture["src"]])
        i+=1
        if i > number:
            break

    break

df = pd.DataFrame(data, columns=["Title", "Description", "Final price", "Rating", "Seller name", "Main image url"])



df.to_csv("data.csv", sep=',', encoding='utf-8')
