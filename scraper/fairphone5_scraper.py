from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList, cleanUpText
from shared.gcs_handler import upload_file
from bs4 import BeautifulSoup
import os
import requests

op = webdriver.ChromeOptions()
# op.add_argument('--headless')
folder = "scraper"

params = {
    "latitude": 50.1109,
    "longitude": -1.92301,
    "accuracy": 100
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}
response = requests.get('https://shop.fairphone.com/fairphone-5', headers=headers)
print(response.url)  # Vergewissere dich, dass es auf Englisch bleibt
# print(response.text)  # HTML-Inhalt





try:
    os.makedirs(f"{folder}/htmls")
except:
    print("folder already exists")

with open(f"{folder}/htmls/fairphone5_source.html", "w", encoding="utf-8") as file:
    file.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")

text = ""
classlist = ["s_fp_wwwww_003 o_colored_level",
             "s_fp_wwwww_004 o_colored_level",
             "s_fp_wwwww_005 o_colored_level",
             "s_fp_wwwww_018 o_colored_level",
             "s_fp_wwwww_019 o_colored_level",
             "s_fp_wwwww_007 o_colored_level",
             "s_fp_wwwww_006 o_colored_level"

             ]
for cl in classlist:
    text = text + soup.find("section", class_=cl).get_text()

cleaned_text = text.replace("\n", " ")

print("-------------------------------------------------------------------------------------------------------------------------------")
# print(all_huawei_products)
fairphoen5_list_for_json:list[dict] = []

fairphoen5_list_for_json.append({"name": "Fairphone 5", "specs": cleaned_text})


filename = "scraped-fairphone-data"
createJsonFromList(fairphoen5_list_for_json, filename)

upload_file("raw_pdf_files", f"{folder}/temp/{filename}.json", f"json_files/{filename}.json")





"""
open page for each phone, scrape text, add {iphone_name, text} to a json file
phile will be called "product_specifics"
"""
