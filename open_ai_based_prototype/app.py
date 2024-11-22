from flask import Flask, render_template, request

from llm_after_class import generateAnswer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", message="")


@app.route('/response', methods=['POST'])
def response():
    name = request.form.get('name')  # Retrieve the 'name' input value
    message = generateAnswer(name)
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
