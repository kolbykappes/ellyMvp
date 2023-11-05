schema = {
  "type": "object",
  "properties": {
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
  "required": ["Job Title", "OEMs", "Technologies", "Skills", "Domains"]
}
