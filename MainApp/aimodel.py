import requests
import json

prompt = """Classify this medical message into ONE category:

emergency - Life-threatening, needs immediate help
(chest pain, bleeding, can't breathe, severe injury, stroke symptoms)

routine - Normal medical care, can wait
(prescription refill, annual checkup, mild symptoms, general health questions)

followup - About previous treatment or appointment  
(medication side effects, post-surgery questions, appointment rescheduling)

other - Not medical or administrative
(billing questions, insurance, "hello", unclear messages, technical issues)

RESPOND WITH ONLY 2 LINES:
[category]
[confidence percentage]

Example:
emergency
95%

NO other text."""


def generate_response(message, model="deepseek-r1:latest"):
    """Generate a response using Ollama API"""
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            response_json = response.json()['message']['content']
            response = response_json.split("</think>")
            return response[1]
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
    except requests.exceptions.ConnectionError:
        raise Exception("Error: Could not connect to Ollama. Make sure Ollama is running on localhost:11434")
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
