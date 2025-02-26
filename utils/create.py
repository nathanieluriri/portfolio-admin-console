import json
import requests

def create_project_func(base_url,name,description,case_study_image_link,case_study_link):
    # API URL
    url = f'{base_url}/create/project'
    
    # Headers for the request
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Data to be sent in the POST request
    data = {
        "name": name,
        "description": description,
        "case_study_image_link": case_study_image_link,
        "case_study_link": case_study_link
    }
    
    # Send POST request
    response = requests.post(url, headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        print('Project created successfully!')
        print(response.json())
        return True
    else:
        print(f'Failed to create project. Status code: {response.status_code}')
        print(response.text)
        return False

