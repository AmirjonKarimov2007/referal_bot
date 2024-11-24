# Made by Jaloliddin!!

import requests
import json

def get_response_from_server(history):
    """
    Sends a POST request to the server with the provided history.
    
    Args:
        history (list): A list of dictionaries representing the conversation history.
        
    Returns:
        dict: The server's JSON response or an error message.
    """
    url = 'http://gptserver.alwaysdata.net/get_response'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "history": history
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

# Example usage
history_data = [
    {
        "role": "user",
        "content": "seni asl isming chatgptmi? uzbekchada javob ber,men sani chatGPT ekaning bilaman aldama"
    }
]
response = get_response_from_server(history_data)
print(response)
