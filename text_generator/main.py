"""
get list of phones
loop through all phones
retrieve texts
upload text to google cloud storage
TODO: remove hashtag preventing file upload
"""
from shared.llm_after_class import generateAnswer
from shared.gcs_handler import download_file_from_bucket, list_files_in_folder, upload_file, create_temp_folder
import json

source_folder = "text_generator"

def access_list_of_phones():
    bucket = "raw_pdf_files"
    json_files = list_files_in_folder(bucket, "json_files")
    print(str(json_files))
    phones = []
    for json_file in json_files:
        if "scraped" in json_file:
            dest: str = f"{source_folder}/temp/{str(json_file).split("/")[1]}"
            download_file_from_bucket(bucket, json_file, dest)
            with open(dest, 'r') as file:
                data: list = json.load(file)

                for el in data:
                    phones.append(el["name"])
    # Replace this list with dynamic data generation logic
    return phones


create_temp_folder()
all_phones = access_list_of_phones()
bucket_name = "raw_pdf_files"



for phone in all_phones:
    resp: str = generateAnswer(phone, source_folder)
    with open(f'{source_folder}/temp/{phone}.html', 'w', encoding='utf-8') as file:
    # Write the string to the file
        file.write(resp)
    upload_file(bucket_name, f'{source_folder}/temp/{phone}.html', f'pre_rendered_texts/{phone}.html')
    print(f"{phone} completed")

    