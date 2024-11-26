from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList, cleanUpText
from gcs_handler import upload_file
from bs4 import BeautifulSoup

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op)

driver.get("https://support.apple.com/en-us/docs/iphone")
html = driver.page_source

driver.implicitly_wait(1)

soup = BeautifulSoup(html, "html.parser")

all_iphone_products: list[BeautifulSoup] = soup.find_all("li", class_="product-list-item")
all_iphone_products_by_text:dict = []

json_content = []

for iphone in all_iphone_products:
    iphone_name = iphone.find("div", class_="product-name").text.strip()
    iphone_link = iphone.find("a")["href"]
    if("iPhone" in iphone_name):
        all_iphone_products_by_text.append({"name": iphone_name, "link": iphone_link})

print(all_iphone_products_by_text)
jsonList = []

for iphone in all_iphone_products_by_text:
    driver.get(iphone["link"])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    try:
        spec_link_el = soup.find("div", class_="docs-product-documentation-techSpecs")
        spec_link = spec_link_el.find("a")["href"]
        driver.get(spec_link)
        
        parent_element = driver.find_element(By.ID, "content")
        pure_text = parent_element.text
        pure_text = cleanUpText(pure_text, "\nLanguages\nLanguage support", "\nIn the Box\n")
        dict_el: dict = {"name": iphone["name"], "specs": pure_text}
    
        jsonList.append(dict_el)
        print(f"""Status: {iphone["name"]} complete""")
    except:
        print(f"""Status: {iphone["name"]} failed""")

filename = "scraped-iphone-data"
createJsonFromList(jsonList, filename)

upload_file("raw_pdf_files", f"temp/{filename}.json", f"json_files/{filename}.json")





"""
open page for each phone, scrape text, add {iphone_name, text} to a json file
phile will be called "product_specifics"
"""
