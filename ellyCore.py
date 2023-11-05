from flask import Flask, render_template, request
import requests
import json
import openai

app = Flask(__name__)

openai.api_key = "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"
OPENAI_URL = "https://api.openai.com/v2/engines/davinci/completions"
API_KEY = "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"

schema = {
  "type": "object",
  "properties": {
    "Match_ID": { "type": "integer" },
    "Job Title": { "type": "string" },
    "OEMs": {
      "type": "array",
      "items": { "type": "string" }
    },
    "Technologies": {
      "type": "array",
      "items": { "type": "string" }
    },
    "Skills": {
      "type": "array",
      "items": { "type": "string" }
    },
    "Summary": { "type": "string" },
    "Domains": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "domain": { "type": "string" },
          "likelihood_percentage": { "type": "number" }
        },
        "required": ["domain", "likelihood_percentage"]
      }    
    }
  },
  "required": ["Match_ID", "Job Title", "OEMs", "Technologies", "Skills", "Domains"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    if app.debug:
        title = "java programmer"
        description = "I need a fancy java dev to write an app"
    else:
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

        # Format the response
        formatted_response = f"<strong>Job Title:</strong> {response_obj['Job Title']}<br>"

        formatted_response += "<strong>Domain:</strong><br><ul>"
        for domain in response_obj['Domains']:
            formatted_response += f"<li>{domain['domain']}: {domain['likelihood_percentage']}%</li>"
        formatted_response += "</ul>"

        formatted_response += "<strong>Technologies:</strong><br><ul>"
        for tech in response_obj['Technologies']:
            formatted_response += f"<li>{tech}</li>"
        formatted_response += "</ul>"

        formatted_response += "<strong>Skills:</strong><br><ul>"
        for skill in response_obj['Skills']:
            formatted_response += f"<li>{skill}</li>"
        formatted_response += "</ul>"

        response_text = formatted_response

    except Exception as e:
        response_text = f"Error: {str(e)}"

    return render_template("index.html", response=response_text, title=title, description=description)


if __name__ == "__main__":
    app.run(debug=True)