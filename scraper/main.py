import subprocess
import os

folder = "scraper"
try:
    os.makedirs(f"{folder}/htmls")
except:
    print("folder already exists")
subprocess.run(["python", "huawai_scraper.py"])
# subprocess.run(["python", "iphone_scraper.py"])
subprocess.run(["python", "mi_scraper.py"])
subprocess.run(["python", "samsung_scraper.py"])