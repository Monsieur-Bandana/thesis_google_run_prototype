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
from shared.score_calculator import main
from shared.json_processor import create_json_file
import json

source_folder = "text_generator"
bucket_name = "raw_pdf_files"
version = "dev"  # enter alterantive names e.g. "dev" here
allow_download = True
test_samples_per_brand = 2


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

                if version != "":
                    data = data[:test_samples_per_brand]
                for el in data:
                    phones.append(el["name"])
    # Replace this list with dynamic data generation logic
    return phones


def create_list_of_already_rendered_phones(score: str) -> list[str]:
    # TODO: adapt after editing
    if version == "dev" and score != "no_score":
        return []
    return_list = []
    file_n = f"generated_reviews_{score}{version}.json"
    if version != "dev" or allow_download:
        download_file_from_bucket(
            bucket_name=bucket_name,
            source_blob_name=f"json_files/{file_n}",
            destination_file_name=f"{source_folder}/temp/{file_n}",
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
    file_ = f"{source_folder}/temp/phones_with_scores-{additive}.json"
    with open(file_, "w") as file:
        # Write the string to the file
        json.dump(list_, file)

    upload_file(
        bucket_name, file_, f"json_files/phones_with_scores_{additive}{version}.json"
    )


def generate_texts():
    all_phones = access_list_of_phones()
    already_rendered_phones = []
    # TODO: decommend later
    already_rendered_phones = create_list_of_already_rendered_phones("no_score")

    for p in already_rendered_phones:
        if p in all_phones:
            all_phones.remove(p)

    update_after_five_phones = 0
    for phone in all_phones:
        outc = generateAnswer(phone, source_folder)
        save_file = f"{source_folder}/temp/generated_reviews_no_score.json"
        create_json_file(outc, "", save_file)

        # "quciksave" after every fifth phone
        if update_after_five_phones % 5 == 0:
            upload_file(
                bucket_name=bucket_name,
                source_file_name=save_file,
                destination_blob_name=f"json_files/generated_reviews_no_score{version}.json",
            )
            generate_scores()
        update_after_five_phones += 1


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
                main.add_entry_to_all_scores_list(
                    all_scores=all_scores,
                    key=key,
                    score=value["score"],
                    save_file1=save_file1,
                    isLocPhone=False,
                )


def generate_scores():
    # reads the list of phones, which have review texts
    with open(f"{source_folder}/temp/generated_reviews_no_score.json", "r") as file:
        all_rendered_phones: list[dict] = json.load(file)
    print(all_rendered_phones)
    print("---------------------------------------")
    # checks which reviewd phones already got scored
    already_scored_phones = create_list_of_already_rendered_phones("with_score")
    print(already_scored_phones)
    for p in already_scored_phones:
        for p_ in all_rendered_phones:
            if p_["name"] == p:
                all_rendered_phones.remove(p_)

    save_file = f"{source_folder}/temp/generated_reviews_with_score.json"
    # calls scoring API for all phones remaining
    for p in all_rendered_phones:
        scored_dic = main._ex(p)
        create_json_file(scored_dic, "", save_file)

    upload_file(
        bucket_name=bucket_name,
        source_file_name=save_file,
        destination_blob_name=f"json_files/generated_reviews_with_score{version}.json",
    )

    # generates and uploads list of all scores (list gets overwritten not updated)
    generateAllScoresList()
    upload_file(
        bucket_name=bucket_name,
        source_file_name=f"{source_folder}/temp/all_scores.json",
        destination_blob_name=f"json_files/all_scores{version}.json",
    )


create_temp_folder(source_folder)
generate_texts()  # executes API calls for review texts loopvice
generate_scores()  # executes API calls for scores loopvice

with open(f"{source_folder}/temp/generated_reviews_with_score.json", "r") as file:
    phones_with_scores = json.load(file)

# sort phones by scores, then extract the best and worse 4 and store them in seperate lists
sorted_scores = sorted(phones_with_scores, key=lambda x: x["conclusion"]["score"])

best_phones = sorted_scores[-4:]
best_phones.reverse()
create_and_upload_json(list_=best_phones, additive="str_best")
worst_phones = sorted_scores[:4]
create_and_upload_json(list_=worst_phones, additive="str_worst")
