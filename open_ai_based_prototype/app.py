from flask import Flask, render_template, request
from gcs_handler import list_files_in_folder, download_file_from_bucket
import json
from llm_after_class import generateAnswer
import random

app = Flask(__name__)

def generate_button_texts():
    bucket = "raw_pdf_files"
    json_files = list_files_in_folder(bucket, "json_files")
    
    phones:list[tuple] = []
    for json_file in json_files:
        if "scraped" in json_file:
            dest: str = f"temp/{str(json_file).split("/")[1]}"
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

                    phones.append((name, f"/static/images/{image}.svg"))
    # Replace this list with dynamic data generation logic
    random.shuffle(phones)

    return phones

def loadAnswer(name):
    bucket = "raw_pdf_files"
    file_content = ""
    download_file_from_bucket(bucket, f"pre_rendered_texts/{name}.html", f"temp/{name}.html")
    try:
        with open(f"temp/{name}.html", 'r') as file:
            # Read the file content
            file_content = file.read()
            return file_content
    except:
        print(f"text could not be extracted from {name}.html")


@app.route("/")
def index():
    button_texts:list[str] = generate_button_texts()

   

    return render_template("index.html", message="", button_texts=button_texts)


@app.route('/response', methods=['POST'])
def response():
    name = request.form.get('name')  # Retrieve the 'name' input value
    try:
        message = loadAnswer(name)
    except:
        print("call api")
        message = generateAnswer(name)
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
