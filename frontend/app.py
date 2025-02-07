from flask import Flask, render_template, jsonify, request
from shared.gcs_handler import list_files_in_folder, download_file_from_bucket, create_temp_folder
from html_generator import generate_html_output
import json
from shared.llm_after_class import generateAnswer
import random
import os
import sys

app = Flask(__name__)
folder = "frontend"
bucket = "raw_pdf_files"
phone_data:list[dict] = []

def generate_buttons_dict(data:list[dict]):
    phones:list[dict] = []
    for el in data:
        name:str = el["name"]
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
    """
    json_files = list_files_in_folder(bucket, "json_files")
    
    phones:list[dict] = []
    for json_file in json_files:
        if "scraped" in json_file and not "companies" in json_file:
            dest: str = f"{folder}/temp/{str(json_file).split("/")[1]}"
            download_file_from_bucket(bucket, json_file, dest)
            with open(dest, 'r') as file:
                data: list[dict] = json.load(file)
    """

    # Replace this list with dynamic data generation logic
    # random.shuffle(phones)

    return generate_buttons_dict(phone_data)

def loadAnswer(name)->str:
    print("----------------->>")
    print(type(phone_data))

    file_content = ""

    for p in phone_data:
        print("----------------->>")
        print(type(p))
        if p["name"] == name:
            file_content = generate_html_output(p)

    return file_content


@app.route("/get-buttons", methods=['GET'])
def responseButtons():
    button_texts:list[dict] = generate_button_texts()
    return button_texts

@app.route("/get-selected-buttons", methods=['POST'])
def responseBestPhones():
    selection_kind = request.form.get('input_text', '') 
    json_file = f"phones_with_scores_str_{selection_kind}.json"
    print(f"-------------------------------------------------------------------------------\n{json_file}")
    dest_file = f"{folder}/temp/{json_file}"
    download_file_from_bucket(bucket, f"json_files/{json_file}", dest_file)
    with open(dest_file, "r") as file:
        data = json.load(file)    
    button_texts:list[dict] = generate_buttons_dict(data)
    return button_texts

@app.before_request
def before_request():
    # Code to run before each request
    create_temp_folder(folder)
    print(f"Before request: {request.path}")
    dest: str = f"{folder}/temp/generated_reviews_with_score.json"
    download_file_from_bucket(bucket_name=bucket, source_blob_name="json_files/generated_reviews_with_score.json", destination_file_name=dest)
    global phone_data
    with open(dest, "r") as file:
        phone_data = json.load(file)
    # Add any other logic you need here

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/get-data', methods=['POST'])
def response():
    name = request.form.get('input_text', '') # Retrieve the 'name' input value
    print("-------------------------->"+name)  
    message = loadAnswer(name)
    if message=="":
        print("call api")
        message = generateAnswer(name, folder)
    return message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
