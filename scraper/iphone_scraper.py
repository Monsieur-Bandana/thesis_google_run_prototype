from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList, cleanUpText
from gcs_handler import upload_file

driver = webdriver.Chrome()

driver.get("https://support.apple.com/en-us/docs/iphone")
driver.implicitly_wait(1)

show_more = driver.find_element(By.CLASS_NAME, "docs-showMore-link")
show_more.find_element(By.CLASS_NAME, "showMoreBtn").click()

driver.implicitly_wait(1)

all_iphone_products = driver.find_elements(By.CLASS_NAME, "product-list-item")
all_iphone_products_by_text:dict = []

json_content = []

for iphone in all_iphone_products:
    iphone_name = iphone.find_element(By.CLASS_NAME, "product-name").text
    iphone_link = iphone.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    all_iphone_products_by_text.append({"name": iphone_name, "link": iphone_link})

jsonList = []

for iphone in all_iphone_products_by_text:
    driver.get(iphone["link"])
    

    # between page
    driver.implicitly_wait(1)
    driver.find_element(By.CLASS_NAME, "docs-product-documentation-techSpecs").find_element(By.CSS_SELECTOR, "a").click()

    # extract specs
    driver.implicitly_wait(1)
    parent_element = driver.find_element(By.ID, "content")
    pure_text = parent_element.text
    pure_text = cleanUpText(pure_text, "\nLanguages\nLanguage support", "\nIn the Box\n")
    dict_el: dict = {"name": iphone["name"], "specs": pure_text}
    
    jsonList.append(dict_el)

filename = "iphone-data"
createJsonFromList(jsonList, "iphone-data")

upload_file("raw-pdf-files", f"temp/{filename}.json", f"json_files/{filename}.json")





"""
open page for each phone, scrape text, add {iphone_name, text} to a json file
phile will be called "product_specifics"
"""
