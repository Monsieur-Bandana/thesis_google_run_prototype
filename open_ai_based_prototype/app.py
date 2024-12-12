from flask import Flask, render_template, jsonify, request
from shared.gcs_handler import list_files_in_folder, download_file_from_bucket, create_temp_folder
import json
from shared.llm_after_class import generateAnswer
import random

app = Flask(__name__)
folder = "open_ai_based_prototype"

def generate_button_texts():
    bucket = "raw_pdf_files"
    json_files = list_files_in_folder(bucket, "json_files")
    
    phones:list[dict] = []
    for json_file in json_files:
        if "scraped" in json_file:
            dest: str = f"{folder}/temp/{str(json_file).split("/")[1]}"
            download_file_from_bucket(bucket, json_file, dest)
            with open(dest, 'r') as file:
                data: list = json.load(file)

                for el in data:
                    name:str = el["name"]
                    text = name.lower()
                    image = ""
                    print(text)
                    if "iphone" in text:
                        image = "iphone"
                    elif "huawei" in text:
                        image = "huawei"
                    else:
                        image = "mi"

                    phones.append({"text": name, "img": f"static/images/{image}.svg"})
    # Replace this list with dynamic data generation logic
    random.shuffle(phones)

    return phones

def loadAnswer(name):
    bucket = "raw_pdf_files"
    file_content = ""
    download_file_from_bucket(bucket, f"pre_rendered_texts/{name}.html", f"{folder}/temp/{name}.html")
    try:
        with open(f"{folder}/temp/{name}.html", 'r') as file:
            # Read the file content
            file_content = file.read()
            return file_content
    except:
        print(f"text could not be extracted from {name}.html")


@app.route("/get-buttons", methods=['GET'])
def responseButtons():
    button_texts:list[dict] = generate_button_texts()

   

    return button_texts

@app.before_request
def before_request():
    # Code to run before each request
    create_temp_folder("open_ai_based_prototype")
    print(f"Before request: {request.path}")
    # Add any other logic you need here

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/get-data', methods=['POST'])
def response():
    name = request.form.get('input_text', '') # Retrieve the 'name' input value
    try:
        message = loadAnswer(name)
    except:
        print("call api")
        message = generateAnswer(name, folder)
    return message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
