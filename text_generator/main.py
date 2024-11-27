"""
get list of phones
loop through all phones
retrieve texts
upload text to google cloud storage
"""
from llm_after_class import generateAnswer
from gcs_handler import download_file_from_bucket, list_files_in_folder, upload_file
import json

def access_list_of_phones():
    bucket = "raw_pdf_files"
    json_files = list_files_in_folder(bucket, "json_files")
    print(str(json_files))
    phones = []
    for json_file in json_files:
        if "scraped" in str(json_file):
            download_file_from_bucket(bucket, json_file, f"temp/{json_file[1]}")
            with open(f"temp/{json_file[1]}", 'r') as file:
                data: list = json.load(file)

                for el in data:
                    phones.append(el["name"])

all_phones = access_list_of_phones()
bucket_name = "raw_pdf_files"
for phone in all_phones[:5]:
    resp: str = generateAnswer(phone)
    with open(f'temp/{phone}.txt', 'w', encoding='utf-8') as file:
    # Write the string to the file
        file.write(resp)
    upload_file(bucket_name, f'temp/{phone}.txt', f'pre_rendered_texts/{phone}.txt')
    print(f"{phone} completed")
    