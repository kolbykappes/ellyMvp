import json

def format_response(completion):
    try:
        response_obj = json.loads(completion.choices[0].message.function_call.arguments)

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

        return formatted_response

    except Exception as e:
        return f"Error: {str(e)}"
