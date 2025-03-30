"""
get list of phones
loop through all phones
retrieve texts
upload text to google cloud storage
TODO: remove hashtag preventing file upload
"""

from shared.llm_after_class import generateAnswer
from shared.gcs_handler import (
    download_file_from_bucket,
    list_files_in_folder,
    upload_file,
    create_temp_folder,
)
import json

source_folder = "text_generator"
bucket_name = "raw_pdf_files"


def access_list_of_phones():
    json_files = list_files_in_folder(bucket_name, "json_files")
    print(str(json_files))
    phones = []
    for json_file in json_files:
        if "scraped" in json_file:
            dest: str = f"{source_folder}/temp/{str(json_file).split("/")[1]}"
            download_file_from_bucket(bucket_name, json_file, dest)
            with open(dest, "r") as file:
                data: list = json.load(file)

                for el in data:
                    phones.append(el["name"])
    return phones


def create_list_of_already_rendered_phones():
    existing_phones: list[str] = list_files_in_folder(bucket_name, "pre_rendered_texts")
    return_list = []
    for phone in existing_phones:
        phone = phone.split("/")[1]
        phone_name = phone.split(".")[0]
        return_list.append(phone_name)
    return return_list


create_temp_folder(source_folder)
all_phones = access_list_of_phones()
already_rendered_phones = []
already_rendered_phones = create_list_of_already_rendered_phones()


for phone in all_phones:
    if not phone in already_rendered_phones:
        resp: str = generateAnswer(phone, source_folder)
        with open(f"{source_folder}/temp/{phone}.html", "w", encoding="utf-8") as file:
            # Write the string to the file
            file.write(resp)
        upload_file(
            bucket_name,
            f"{source_folder}/temp/{phone}.html",
            f"pre_rendered_texts/{phone}.html",
        )
        print(f"{phone} completed")
    else:
        print(f"{phone} got already generated")
