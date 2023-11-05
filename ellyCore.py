from flask import Flask, render_template, request
import requests
import json
import openai
from response_formatter import format_response
from schema import schema

app = Flask(__name__)

openai.api_key = "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"
OPENAI_URL = "https://api.openai.com/v2/engines/davinci/completions"
API_KEY = "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"

@app.route("/", methods=["GET", "POST"])
def index():
    title = ""
    description = ""
    response_text = ""

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        if app.debug and not title and not description:
            title = "java programmer"
            description = "I need a fancy java dev to write an app"

        with open("prompt.txt", "r") as f:
            base_prompt = f.read()

        prompt = base_prompt + " " + title + " " + description
        # ... [rest of the API call logic]

        completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant with lots of IT experience and HR experience."},
                {"role": "user", "content": prompt}
            ],
            functions=[{"name": "set_job_results", "parameters": schema}],
            function_call={"name": "set_job_results"},
            temperature=0
        )

        try:
            response_obj = json.loads(completion.choices[0].message.function_call.arguments)
            print("OpenAI Response:", response_obj)

            response_text = format_response(completion)

        except Exception as e:
            response_text = f"Error: {str(e)}"

    return render_template("index.html", response=response_text, title=title, description=description)

if __name__ == "__main__":
    app.run(debug=True)
