"""
get list of phones
loop through all phones
retrieve texts
upload text to google cloud storage
TODO: remove hashtag preventing file upload
"""

from shared.llm_after_class import generateAnswer
from shared.gcs_handler import download_file_from_bucket, list_files_in_folder, upload_file, create_temp_folder
from score_calculator import main
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
            with open(dest, 'r') as file:
                data: list = json.load(file)
                #TODO: remove limit
                for el in data[:1]:
                    phones.append(el["name"])
    # Replace this list with dynamic data generation logic
    return phones

def create_list_of_already_rendered_phones():
    existing_phones: list[str] = list_files_in_folder(bucket_name, "pre_rendered_texts_c")
    return_list = []
    for phone in existing_phones:
        phone = phone.split("/")[1]
        phone_name = phone.split(".")[0]
        return_list.append(phone_name)
    return return_list

def create_and_upload_json(list_, additive=""):
    file_ = f'{source_folder}/temp/phones_with_scores-{additive}.json'
    with open(file_, 'w') as file:
    # Write the string to the file
        json.dump(list_, file)

    # upload_file(bucket_name, file_, f'json_files/phones_with_scores_{additive}.json')

create_temp_folder(source_folder)
all_phones = access_list_of_phones()
already_rendered_phones = []
already_rendered_phones = create_list_of_already_rendered_phones()


for phone in all_phones:
    if not phone in already_rendered_phones:
        resp: dict = generateAnswer(phone, source_folder, False)
        main._ex(resp)

    else:
        print(f"{phone} got already generated")
with open("generated_reviews_with_score.json", "r") as file:

    phones_with_scores = json.load(file)

sorted_scores = sorted(phones_with_scores, key=lambda x: x['conclusion']['score'])

best_phones = sorted_scores[-4:]
best_phones.reverse()
create_and_upload_json(list_=best_phones, additive="best")
worst_phones = sorted_scores[:4]
create_and_upload_json(list_=worst_phones, additive="worst")