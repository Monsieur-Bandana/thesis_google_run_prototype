"""
get list of phones
loop through all phones
retrieve texts
upload text to google cloud storage
TODO: remove hashtag preventing file upload
"""

from shared.llm_after_class import generateAnswer
from shared.gcs_handler import download_file_from_bucket, list_files_in_folder, upload_file, create_temp_folder
from shared.score_calculator import main
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

def create_list_of_already_rendered_phones_depriciated():
    existing_phones: list[str] = list_files_in_folder(bucket_name, "pre_rendered_texts_c")
    return_list = []
    for phone in existing_phones:
        phone = phone.split("/")[1]
        phone_name = phone.split(".")[0]
        return_list.append(phone_name)
    return return_list

def create_list_of_already_rendered_phones(score: str) -> list[str]:
    # TODO: adapt after editing
    return []
    return_list = []
    file_n = f"generated_reviews_{score}.json"
    download_file_from_bucket(
        bucket_name=bucket_name,
        source_blob_name=f"json_files/{file_n}",
        destination_file_name=f"{source_folder}/temp/{file_n}"
    )
    try:
        with open(f"{source_folder}/temp/{file_n}", "r") as file:
            already_rendered_phones = json.load(file)
        for el in already_rendered_phones:
            return_list.append(el["name"])
        return return_list
    except:
        return []


def create_and_upload_json(list_, additive=""):
    file_ = f'{source_folder}/temp/phones_with_scores-{additive}.json'
    with open(file_, 'w') as file:
    # Write the string to the file
        json.dump(list_, file)

    upload_file(bucket_name, file_, f'json_files/phones_with_scores_{additive}.json')

def generate_texts():
    all_phones = access_list_of_phones()
    already_rendered_phones = []
    # TODO: decommend later
    # already_rendered_phones = create_list_of_already_rendered_phones("no_score")

    for p in already_rendered_phones:
        if p in all_phones:
            all_phones.remove(p)

    for phone in all_phones:
        generateAnswer(phone, source_folder)
    # generateAnswer saves file "generated_reviews_no_score.json"

    upload_file(bucket_name=bucket_name, source_file_name=f"{source_folder}/temp/generated_reviews_no_score.json", destination_blob_name=f"json_files/generated_reviews_no_score.json")

def generateAllScoresList():
    file_n = f"{source_folder}/temp/generated_reviews_with_score.json"
    save_file1 = f"{source_folder}/temp/all_scores.json"
    all_scores = {}
    with open(file_n, "r") as file:
        scored_phones = json.load(file)
    for sc_p in scored_phones:
        dicti: dict = sc_p

        for key, value in dicti.items():
            if isinstance(value, dict):
                main.add_entry_to_all_scores_list(all_scores=all_scores, key=key, score=value["score"], save_file1=save_file1, isLocPhone=False)

    


def generate_scores():
    download_file_from_bucket("raw_pdf_files", f"json_files/all_scores.json", f"{source_folder}/temp/all_scores.json")
    with open(f"{source_folder}/temp/generated_reviews_no_score.json", "r") as file:
        all_rendered_phones:list[dict] = json.load(file)
    print(all_rendered_phones)
    print("---------------------------------------")
    already_scored_phones = create_list_of_already_rendered_phones("with_score")
    print(already_scored_phones)
    for p in already_scored_phones:
        for p_ in all_rendered_phones:
            if p_["name"]==p:
                all_rendered_phones.remove(p_)

    for p in all_rendered_phones:
        main._ex(p, "text_generator")

    upload_file(bucket_name=bucket_name, source_file_name=f"{source_folder}/temp/generated_reviews_with_score.json", destination_blob_name=f"json_files/generated_reviews_with_score.json")
    generateAllScoresList()
    upload_file(bucket_name=bucket_name, source_file_name=f"{source_folder}/temp/all_scores.json", destination_blob_name=f"json_files/all_scores.json")


create_temp_folder(source_folder)
generate_texts()
generate_scores()

with open(f"{source_folder}/temp/generated_reviews_with_score.json", "r") as file:
    phones_with_scores = json.load(file)

sorted_scores = sorted(phones_with_scores, key=lambda x: x['conclusion']['score'])

best_phones = sorted_scores[-4:]
best_phones.reverse()
create_and_upload_json(list_=best_phones, additive="str_best")
worst_phones = sorted_scores[:4]
create_and_upload_json(list_=worst_phones, additive="str_worst")