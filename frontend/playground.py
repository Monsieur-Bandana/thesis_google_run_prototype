from flask import Flask, render_template, jsonify, request
from shared.gcs_handler import list_files_in_folder, download_file_from_bucket, create_temp_folder
import json
from shared.llm_after_class import generateAnswer
import random
import os

app = Flask(__name__)
folder = "frontend"


@app.route('/')
def index():
    return render_template('playground.html') 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
