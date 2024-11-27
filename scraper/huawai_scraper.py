from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList, cleanUpText
from gcs_handler import upload_file
from bs4 import BeautifulSoup
import os

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op)

driver.get("https://consumer.huawei.com/en/sitemap/")
html = driver.page_source

try:
    os.makedirs("htmls")
except:
    print("folder already exists")

with open("htmls/huawai_page_source.html", "w", encoding="utf-8") as file:
    file.write(html)

driver.implicitly_wait(1)

soup = BeautifulSoup(html, "html.parser")

sections: BeautifulSoup = soup.find_all("ul", "sitmap-mainul")[1]
smartphone_section = sections.find("li", "sitmap-mainitem")
all_huawai_products:list[BeautifulSoup] = smartphone_section.find_all("p", class_="sitmap-subitem-p")
print("-------------------------------------------------------------------------------------------------------------------------------")
# print(all_huawai_products)
all_huawai_phones:list[dict] = []

json_content = []

for phone in all_huawai_products:
    
    phone_link = phone.find("a")["href"]
    phone_title = phone.find("a")["act"]
    if("phones" in phone_link):
        all_huawai_phones.append({"name": phone_title,"link": f"{phone_link}specs/"})

print(all_huawai_phones)
jsonList:list[dict] = []

for phone in all_huawai_phones:
    driver.get(phone["link"])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    outc_text = soup.find("ul", class_="large-accordion__list").text
    cleaned_text = outc_text.replace("\n", " ")
    jsonList.append({"name": phone["name"],"specs": cleaned_text})

filename = "scraped-huawai-data"
createJsonFromList(jsonList, filename)

upload_file("raw_pdf_files", f"temp/{filename}.json", f"json_files/{filename}.json")





"""
open page for each phone, scrape text, add {iphone_name, text} to a json file
phile will be called "product_specifics"
"""