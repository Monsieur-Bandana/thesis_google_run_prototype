from flask import Flask, render_template, request, redirect, url_for

from boot_up_llm import boot_model
from llm import generateAnswer

app = Flask(__name__)

model, tokenizer = boot_model()

@app.route("/")
def index():
    return render_template("index.html", message="")


@app.route('/response', methods=['POST'])
def response():
    name = request.form.get('name')  # Retrieve the 'name' input value
    message = generateAnswer(name, model, tokenizer)
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
