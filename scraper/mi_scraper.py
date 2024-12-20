from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList
from shared.gcs_handler import upload_file
from bs4 import BeautifulSoup
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def exec_scrape(scrape_link):
    driver.get(scrape_link)
    html = driver.page_source

    try:
        os.makedirs("scraper/htmls")
    except:
        print("folder already exists")

    with open("scraper/htmls/mi_page_source.html", "w", encoding="utf-8") as file:
        file.write(html)


    driver.implicitly_wait(2)

    soup = BeautifulSoup(html, "html.parser")

    sections: list[BeautifulSoup] = soup.find_all("bdi")
    links: list[BeautifulSoup] = soup.find_all("div", class_="item__action")
    print(str(len(sections)))
    print(str(len(links)))

    # print(all_huawei_products)
    all_mi_phones:list[dict] = []

    i = 0
    for phone in sections:
        
        phone_name: str = phone.get_text()
        link: BeautifulSoup = links[i]
        phone_link = link.find("a")["href"]
        
        all_mi_phones.append({"name": phone_name,"link": f"{phone_link}specs"})
        i+=1


    for phone in all_mi_phones:
        driver.get(phone["link"])
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "specs-con")))
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            outc_text = soup.find("div", class_="specs-con").text
            cleaned_text = outc_text.replace("\n", " ")
            jsonList.append({"name": phone["name"],"specs": cleaned_text})
        except:
            print(f"couldn't find specs-class for {phone['name']}")


jsonList:list[dict] = []
op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op)
exec_scrape("https://www.mi.com/en/product-list/phone/redmi/")
exec_scrape("https://www.mi.com/en/product-list/phone/xiaomi/")
filename = "scraped-mi-data"
createJsonFromList(jsonList, filename)

upload_file("raw_pdf_files", f"scraper/temp/{filename}.json", f"json_files/{filename}.json")
driver.quit()







"""
open page for each phone, scrape text, add {iphone_name, text} to a json file
phile will be called "product_specifics"
"""
