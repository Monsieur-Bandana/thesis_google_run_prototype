from flask import Flask, render_template, jsonify, request
from shared.gcs_handler import list_files_in_folder, download_file_from_bucket, create_temp_folder
import json
from shared.llm_after_class import generateAnswer
import random
import os

app = Flask(__name__)
folder = "frontend"
bucket = "raw_pdf_files"

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
    json_files = list_files_in_folder(bucket, "json_files")
    
    phones:list[dict] = []
    for json_file in json_files:
        if "scraped" in json_file and not "companies" in json_file:
            dest: str = f"{folder}/temp/{str(json_file).split("/")[1]}"
            download_file_from_bucket(bucket, json_file, dest)
            with open(dest, 'r') as file:
                data: list[dict] = json.load(file)

                phones = phones + generate_buttons_dict(data)
    # Replace this list with dynamic data generation logic
    # random.shuffle(phones)

    return phones

def loadAnswer(name)->str:
    bucket = "raw_pdf_files"
    file_content = ""
    file_path = f"{folder}/temp/{name}.html"

    # download json
    # find element or maybe el is in name
    # generate_html_anser
    try:
        download_file_from_bucket(bucket, f"pre_rendered_texts_c/{name}.html", file_path)

        with open(file_path, 'r') as file:

            file_content = file.read()
            return file_content
        
    except:
        # workarround: try block created empty file, causing bug. remove file to prevent bug
        if os.path.exists(file_path):
            os.remove(file_path)

        print(f"text could not be extracted from {name}.html")

    return file_content


@app.route("/get-buttons", methods=['GET'])
def responseButtons():
    button_texts:list[dict] = generate_button_texts()
    return button_texts

@app.route("/get-selected-buttons", methods=['POST'])
def responseBestPhones():
    selection_kind = request.form.get('input_text', '') 
    json_file = f"phones_with_scores_{selection_kind}.json"
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
    # Add any other logic you need here

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/get-data', methods=['POST'])
def response():
    name = request.form.get('input_text', '') # Retrieve the 'name' input value
    
    message = loadAnswer(name)
    if message=="":
        print("call api")
        message = generateAnswer(name, folder)
    return message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
