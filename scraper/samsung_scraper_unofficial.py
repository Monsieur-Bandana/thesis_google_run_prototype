from selenium import webdriver
from selenium.webdriver.common.by import By
from json_handler import createJsonFromList, cleanUpText
from shared.gcs_handler import upload_file
from bs4 import BeautifulSoup
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



op = webdriver.ChromeOptions()
# op.add_argument('--headless')
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
op.add_argument(f"user-agent={user_agent_string}")
driver = webdriver.Chrome(options=op)

samsung_link = "https://www.gsmarena.com/samsung-phones-9.php"
driver.implicitly_wait(5)

driver.get(samsung_link)

html = driver.page_source

try:
    os.makedirs("htmls")
except:
    print("folder already exists")

with open("scraper/htmls/samsung_page_source.html", "w", encoding="utf-8") as file:
    file.write(html)


soup = BeautifulSoup(html, "html.parser")

parent = soup.find("div", class_="makers")

sections: list[BeautifulSoup] = parent.find_all("li")
print(len(sections))


all_samsung_phones:list[dict] = []

json_content = []

print(len(sections))
for phone in sections:
    print(phone.prettify())
    
    phone_link = phone.find("a")["href"]
    phone_title = phone.find("span").get_text()
    if not "Watch" in phone_title:
        all_samsung_phones.append({"name": phone_title,"link": f"https://www.gsmarena.com/{phone_link}"})

print(len(all_samsung_phones))
jsonList:list[dict] = []
scd_try_list = []

i: int = 0
for phone in all_samsung_phones:
    
    driver.get(phone["link"])
    if i < 5:
        driver.implicitly_wait(1)
    else:
        driver.implicitly_wait(7)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        outc_text = soup.find("div",{'id': 'specs-list'}).text
        cleaned_text = outc_text.replace("\n", " ")
        jsonList.append({"name": phone["name"],"specs": cleaned_text})
    except:
        print(f"""couldn't find data for {phone["name"]}""")
    i+=1


"""
for phone in scd_try_list:
    
    try:
        exec_text_pull(phone)
    except:
        print(f"couldn't find specs data of {phone['name']} in scd ty as well")


"""
filename = "scraped-samsung-data"
createJsonFromList(jsonList, filename)

# upload_file("raw_pdf_files", f"temp/{filename}.json", f"json_files/{filename}.json")