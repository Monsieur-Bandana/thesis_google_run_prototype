from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList
from gcs_handler import upload_file
from bs4 import BeautifulSoup
import os


def exec_scrape(scrape_link):
    driver.get(scrape_link)
    html = driver.page_source

    try:
        os.makedirs("htmls")
    except:
        print("folder already exists")

    with open("htmls/mi_page_source.html", "w", encoding="utf-8") as file:
        file.write(html)


    driver.implicitly_wait(2)

    soup = BeautifulSoup(html, "html.parser")

    sections: list[BeautifulSoup] = soup.find_all("bdi")
    links: list[BeautifulSoup] = soup.find_all("div", class_="item__action")
    print(str(len(sections)))
    print(str(len(links)))

    # print(all_huawei_products)
    all_mi_phones:list[dict] = []

    json_content = []

    i = 0
    for phone in sections:
        
        phone_name: str = phone.get_text()
        link: BeautifulSoup = links[i]
        phone_link = link.find("a")["href"]
        
        all_mi_phones.append({"name": phone_name,"link": f"{phone_link}specs"})
        i+=1

    jsonList:list[dict] = []

    for phone in all_mi_phones:
        driver.get(phone["link"])
        driver.implicitly_wait(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        outc_text = soup.find("div", class_="specs-con").text
        cleaned_text = outc_text.replace("\n", " ")
        jsonList.append({"name": phone["name"],"specs": cleaned_text})

    filename = "scraped-mi-data"
    createJsonFromList(jsonList, filename)

    upload_file("raw_pdf_files", f"temp/{filename}.json", f"json_files/{filename}.json")

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome()
exec_scrape("https://www.mi.com/en/product-list/phone/redmi/")
exec_scrape("https://www.mi.com/en/product-list/phone/xiaomi/", 'a')







"""
open page for each phone, scrape text, add {iphone_name, text} to a json file
phile will be called "product_specifics"
"""
