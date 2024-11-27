from flask import Flask, render_template, request
from gcs_handler import list_files_in_folder, download_file_from_bucket
import json

app = Flask(__name__)

def generate_button_texts():
    bucket = "raw_pdf_files"
    json_files = list_files_in_folder(bucket, "json_files")
    print(str(json_files))
    phones = []
    for json_file in json_files:
        if "scraped" in str(json_file):
            download_file_from_bucket(bucket, json_file, f"temp/{json_file[1]}")
            with open(f"temp/{json_file[1]}", 'r') as file:
                data: list = json.load(file)

                for el in data:
                    phones.append(el["name"])
    # Replace this list with dynamic data generation logic
    return phones

def loadAnswer(name):
    bucket = "raw_pdf_files"
    file_content = ""
    download_file_from_bucket(bucket, f"pre_rendered_texts/{name}.txt", f"temp/{name}.txt")
    with open(f"temp/{name}", 'r', encoding='utf-8') as file:
        # Read the file content
        file_content = file.read()

    return file_content


@app.route("/")
def index():
    button_texts = generate_button_texts()
    return render_template("index.html", message="", button_texts=button_texts)


@app.route('/response', methods=['POST'])
def response():
    name = request.form.get('name')  # Retrieve the 'name' input value
    message = loadAnswer(name)
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
