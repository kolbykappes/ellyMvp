from flask import Flask, render_template, request
import requests
import json
import openai

app = Flask(__name__)

openai.api_key = "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"
OPENAI_URL = "https://api.openai.com/v2/engines/davinci/completions"

# Assuming you have the schema in a separate file called schema.py
from schema import schema

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

        with open("prompt2.txt", "r") as f:
            base_prompt = f.read()

        prompt = base_prompt + " " + title + " " + description

        completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
#            model="gpt-3.5-turbo",            
            messages=[
                {"role": "system", "content": "You are a helpful assistant with lots of IT experience and HR experience."},
                {"role": "user", "content": prompt}
            ],
            functions=[{"name": "set_job_results", "parameters": schema}],
            function_call={"name": "set_job_results"},
            temperature=0
        )

        # Print the entire response to the console
        print("OpenAI API Response:", completion)

        if 'choices' in completion:
            response_str = completion['choices'][0]['message']['function_call']['arguments']
            # Assuming you have the format_response function in a separate file called response_formatter.py
            from response_formatter import format_response
            response_text = format_response(response_str)
        else:
            response_text = "Error: 'choices' not found in the response."

    # Determine whether to show the Elly's Response section
    if response_text:
        response_section_display = 'block'
    else:
        response_section_display = 'none'

    return render_template("index.html", response=response_text, formatted_response2="Resp2", formatted_response3="Resp3", title=title, description=description, response_section_display=response_section_display)

if __name__ == "__main__":
    app.run(debug=True)
