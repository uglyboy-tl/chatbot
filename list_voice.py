import requests

from config import minimax_api_key

url = 'https://api.minimax.chat/v1/get_voice'
headers = {
    'authority': 'api.minimax.chat',
    'Authorization': f'Bearer {minimax_api_key}'
}

data = {
    'voice_type': 'voice_cloning'
}

response = requests.post(url, headers=headers, data=data)
print(response.text)