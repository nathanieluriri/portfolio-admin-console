

import json
import requests

def get_contact_func(base_url):
    messages =[]
    # API URL
    url = f'{base_url}/get/messages'
    
    # Headers for the request
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    

    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        res = response.json()
        for r in res.get('messages'):
            r = r.replace("'",'"')
            message_str= json.loads(r)
            messages.append(message_str)
            
        return messages
    else:
        print(f'Failed to create project. Status code: {response.status_code}')
        print(response.text)
        return False




def delete_contact_func(base_url,contact_id):
       # API URL with project ID to delete
    url = f'{base_url}/delete/contact/{contact_id}'
    
    # Headers for the request
    headers = {
        'accept': 'application/json'
    }
    
    # Send DELETE request
    response = requests.delete(url, headers=headers)
    print(response)
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f'Contact Message {contact_id} deleted successfully!')
        print(response.json())  # Optional: If the response contains data
        return True
    else:
        print(f'Failed to delete Message. Status code: {response.status_code}')
        print(response.text)  # Print the error message
        return False

# Example usage

# get_contact_func(base_url="http://127.0.0.1:8000/v1/product-design")

# delete_contact_func(base_url="http://127.0.0.1:8000/v1/product-design",contact_id="67bfb6ea55b544ac5f6d87ee")