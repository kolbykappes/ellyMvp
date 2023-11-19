schema = {
    "type": "object",
    "properties": {
      "Job Title": { "type": "string" },
      "Skills": {
        "type": "array",
        "items": { "type": "string" }
      },
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
      },
      "PossibleIssues": {
        "type": "array",
        "items": { "type": "string" }
      }
    },
    "required": ["Job Title", "OEMs", "Technologies", "Skills", "Domains"]
  }