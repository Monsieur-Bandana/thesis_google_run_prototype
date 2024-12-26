import json
import os
from shared.gcs_handler import upload_file

def get_classification_json_files(folder_path):
    """
    Get all files in a folder that are JSON files and have 'classification' in their name.

    :param folder_path: Path to the folder to search in.
    :return: List of matching file paths.
    """
    matching_files: list[str] = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('classification.json'):
            matching_files.append(os.path.join(folder_path, file_name))
    json_list: list[dict] = []
    for mfile in matching_files:
        with open(mfile, 'r') as file:
            data: list[dict] = json.load(file)
            for date in data:
                category:str = mfile.split("-")[0]
                category:str = category.split("\\")[1]
                date["category"] = category
            json_list = json_list + data
    
    return json_list


def add_footnotes(folder_name, classes):
    sources_list: list = get_classification_json_files(f"{folder_name}/temp")


    footnotes_all: list[list] = []
    for ent in classes:
        footnotes: list[dict] = []
        length: int = len(sources_list)
        i: int = 1
        for i in range(length):
            if ent in sources_list[i]["labels"]:
                footnotes.append({"category": sources_list[i]["category"], "footnote": i})
            i = i + 1
        footnotes_all.append({"name": ent, "footnotes": footnotes})

    with open(f"{folder_name}/temp/footnotes.json", "w") as file:
        json.dump(footnotes_all, file, indent=4)

    upload_file("raw_pdf_files", f"{folder_name}/temp/footnotes.json","json_files/footnotes.json")


# den folgenden part später importieren lassen >>>

folder_name = "file_classifier"
classes = []

with open(f'{folder_name}/temp/classes.json', 'r') as file:
    data: list = json.load(file)

    for el in data:
        classes.append(el["name"])

sources_list: list = get_classification_json_files(f"{folder_name}/temp")
json_file: list[dict] = []
i = 1
for sel in sources_list:
    ...
# <<< bis hierhin