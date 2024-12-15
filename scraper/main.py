import subprocess
import os
from json_handler import createJsonFromList
from shared.gcs_handler import upload_file

folder = "scraper"
try:
    os.makedirs(f"{folder}/htmls")
except:
    print("folder already exists")

jsonList = []
# subprocess.run(["python", "huawai_scraper.py"])
jsonList.append("huawei")
# subprocess.run(["python", "iphone_scraper.py"])
jsonList.append("iphone")
# subprocess.run(["python", "mi_scraper.py"])
jsonList.append("mi")
# subprocess.run(["python", "samsung_scraper.py"])
jsonList.append("samsung")

jsonList.append("fairphone")
createJsonFromList(jsonList, "scraped_companies")
upload_file("raw_pdf_files", f"{folder}/temp/scraped_companies.json", "json_files/scraped_companies.json" )