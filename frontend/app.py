from flask import Flask, render_template, request
from shared.gcs_handler import (
    download_file_from_bucket,
    create_temp_folder,
)
from html_generator import generate_html_output, generate_table_output
import json
from shared.llm_after_class import generateAnswer
from shared.score_calculator import main

app = Flask(__name__)

# set here if you want to retreive files from dev versions, set "" if you want the normal version
version = ""  # or dev
folder = "frontend"
bucket = "raw_pdf_files"
# list of all phones, gets filled by before_request function
phone_data: list[dict] = []
# scores of all phones (important for the ratio bar), gets filled by before_request function
all_phones_scores = {}
# if compare-mode this variable stores the orignal phone
phone_one = {}


# laods the correct brand-icons for the phone buttons from the image gallery
def generate_buttons_dict(data: list[dict]):
    phones: list[dict] = []
    for el in data:
        name: str = el["name"]
        text = name.lower()
        image = ""
        print(text)
        if "iphone" in text:
            image = "iphone"
        elif "huawei" in text:
            image = "huawei"
        elif "fairphone" in text:
            image = "fairphone"
        elif "galaxy" in text:
            image = "samsung"
        else:
            image = "mi"

        phones.append({"text": name, "img": f"static/images/{image}.svg"})
    return phones


def generate_button_texts():

    return generate_buttons_dict(phone_data)


# loads the review text
def loadAnswer(name, mode) -> str:
    """
    :param name: model name
    :param mode: compare mode ("2") or single mode ("")
    :return: html version of review text as String
    """

    file_content = ""

    # api call if phone does not exist
    def create_new_phone():
        new_p = generateAnswer(name, folder, 2)

        new_P_w_sc = main._ex(new_p)

        phone_one = new_P_w_sc
        return phone_one

    # checks if phone exists, either returns phone or calls api, if not existant
    def quickLoop():
        for p in phone_data:
            print(type(p))
            if p["name"] == name:
                p["in_list"] = "true"  # checks if in scores list
                return p
        p = create_new_phone()
        p["in_list"] = "false"
        return p

    # checks if normal mode or compare mode (2)
    if mode == "":
        p = quickLoop()
        global phone_one
        phone_one = p
        if p:
            file_content = generate_html_output(p, all_phones_scores)
    elif mode == "2":
        p = quickLoop()
        if p:
            file_content = generate_table_output(phone_one, p, all_phones_scores)

    return file_content


@app.route("/get-buttons", methods=["GET"])
def responseButtons():
    button_texts: list[dict] = generate_button_texts()
    return button_texts


@app.route("/get-selected-buttons", methods=["POST"])
def responseBestPhones():
    selection_kind = request.form.get("input_text", "")
    json_file = f"phones_with_scores_str_{selection_kind}{version}.json"

    dest_file = f"{folder}/temp/{json_file}"
    download_file_from_bucket(bucket, f"json_files/{json_file}", dest_file)
    with open(dest_file, "r") as file:
        data = json.load(file)
    button_texts: list[dict] = generate_buttons_dict(data)
    return button_texts


@app.before_request
def before_request():
    """
    Code to run before each request, loads all files needed for enabling the frontend, list of all phones, worst phones, best phones
    list of all scores

    """
    create_temp_folder(folder)
    print(f"Before request: {request.path}")
    dest: str = f"{folder}/temp/generated_reviews_with_score.json"
    download_file_from_bucket(
        bucket_name=bucket,
        source_blob_name=f"json_files/generated_reviews_with_score{version}.json",
        destination_file_name=dest,
    )
    global phone_data
    with open(dest, "r") as file:
        phone_data = json.load(file)
    dest2 = f"{folder}/temp/all_scores.json"
    download_file_from_bucket(
        bucket_name=bucket,
        source_blob_name=f"json_files/all_scores{version}.json",
        destination_file_name=dest2,
    )
    global all_phones_scores
    with open(dest2, "r") as file:
        all_phones_scores = json.load(file)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-data", methods=["POST"])
def response():
    """
    retrieves request from frontend. the requests contains a string, seperated by comma. the string contains before the comma the model name,
    behind the comma information about the mode (compare vs normal)
    """
    requ_l = request.form.get("input_text", "").split(",")
    name = requ_l[0]
    mode = requ_l[1]
    message = loadAnswer(name, mode)

    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
