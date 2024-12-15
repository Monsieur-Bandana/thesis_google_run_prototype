from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList, cleanUpText
from shared.gcs_handler import upload_file
from bs4 import BeautifulSoup
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def exec_text_pull(phone, el, classn):
    driver.get(phone["link"])
    print(f"calling page {phone["link"]} ...")

    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
  
    parent_el: BeautifulSoup = soup.find(el, class_=classn)
    print(parent_el)
    inner_html = str(parent_el.get_text())
    # print(f"text starts here: {inner_html} and ends here")
    
    cleaned_text = inner_html.replace("\n", " ")
    json_content.append({"name": phone["name"],"debug_info": {"used_link": phone["link"], "el_name": el, "class_name": classn},"specs": cleaned_text})


op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome()

series_list: list[str] = ["s", "a", "m"]
json_content: list[dict] = []

try:
    os.makedirs("htmls")
except:
    print("folder already exists")

for part in series_list:
    samsung_link = f"https://www.samsung.com/uk/smartphones/galaxy-{part}/"
    try:

        driver.implicitly_wait(5)

        driver.get(samsung_link)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pd03-product-card__product-name"))
        )
        html = driver.page_source

        with open("scraper/htmls/samsung_page_source.html", "w", encoding="utf-8") as file:
            file.write(html)


        soup = BeautifulSoup(html, "html.parser")

        sections: list[BeautifulSoup] = soup.find_all("div", class_='pd03-product-card__product-name')
        print(len(sections))


        all_samsung_phones:list[dict] = []


        for phone in sections:
            
            phone_link = phone.find("a")["href"]
            phone_title = phone.find("a")["aria-label"]
            all_samsung_phones.append({"name": phone_title,"link": f"https://www.samsung.com{phone_link}specs/"})

        print(all_samsung_phones)
        scd_try_list = []

        for phone in all_samsung_phones:
            
            try:
                exec_text_pull(phone, "div", "specification__inner")
            except:
                print(f"couldn't find specs data of {phone['name']} --> adding to scd list")
                new_link = str(phone['link']).replace("specs", "#specs")
                phone["link"] = new_link
                scd_try_list.append(phone)
        print(str(scd_try_list))

        for phone in scd_try_list:
            
            try:
                exec_text_pull(phone, "section", "spec-highlight")
                
            except:
                print(f"couldn't find specs data of {phone['name']} in scd ty as well")
    except:
        print(f"{samsung_link} can't be reached")


filename = "scraped-galaxy-data"
createJsonFromList(json_content, filename)

upload_file("raw_pdf_files", f"temp/{filename}.json", f"json_files/{filename}.json")