import requests
import json

# Test the chatbot API
url = 'http://127.0.0.1:8000/chat/send-message/'

# First message
payload = {
    'message': 'Hello! What are the core courses in Civil Engineering?',
    'session_id': ''
}

response = requests.post(url, json=payload)
data = response.json()

print("Bot Response:", data.get('bot_response'))
print("Session ID:", data.get('session_id'))
print("\n" + "="*50 + "\n")

# Second message with session
payload2 = {
    'message': 'How long is the program?',
    'session_id': data.get('session_id')
}

response2 = requests.post(url, json=payload2)
data2 = response2.json()

print("Bot Response:", data2.get('bot_response'))