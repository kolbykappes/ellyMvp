import json

def format_response(response_str):
    try:
#        print ("in format response - input:" + completion)
#        response_obj = json.loads(completion.choices[0].message.function_call.arguments)
#        print ("in format response - post format:" + response_obj)
#        response_obj = completion
        completion = json.loads(response_str)

        # Format the response
        formatted_response = f"<strong>Job Title:</strong> {completion['Job Title']}<br>"

        formatted_response += "<strong>Domain:</strong><br><ul>"
        for domain in completion['Domains']:
            formatted_response += f"<li>{domain['domain']}: {domain['likelihood_percentage']}%</li>"
        formatted_response += "</ul>"

        formatted_response += "<strong>Technologies:</strong><br><ul>"
        for tech in completion['Technologies']:
            formatted_response += f"<li>{tech}</li>"
        formatted_response += "</ul>"

        formatted_response += "<strong>Skills:</strong><br><ul>"
        for skill in completion['Skills']:
            formatted_response += f"<li>{skill}</li>"
        formatted_response += "</ul>"

        return formatted_response

    except Exception as e:
        return f"Error: {str(e)}"
