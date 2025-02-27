

import json
import requests

def get_project_func(base_url,project_id):
    # API URL
    url = f'{base_url}/get/project/{project_id}'
    
    # Headers for the request
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    

    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        print('Project created successfully!')
        print(response.json())
        return response.json()
    else:
        print(f'Failed to create project. Status code: {response.status_code}')
        print(response.text)
        return False

