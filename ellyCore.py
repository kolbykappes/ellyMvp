from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

OPENAI_URL = "https://api.openai.com/v2/engines/davinci/completions"
API_KEY = "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"

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        with open("prompt.txt", "r") as f:
            base_prompt = f.read()

        prompt = base_prompt + " " + title + " " + description

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "prompt": prompt,
            "max_tokens": 250
        }

        response = requests.post(OPENAI_URL, headers=headers, data=json.dumps(data))
        response_text = response.json()["choices"][0]["text"].strip()

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
