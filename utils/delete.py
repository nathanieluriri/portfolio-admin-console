import requests

def delete_project_func(base_url,project_id):
    # API URL with project ID to delete
    url = f'{base_url}/delete/project/{project_id}'
    
    # Headers for the request
    headers = {
        'accept': 'application/json'
    }
    
    # Send DELETE request
    response = requests.delete(url, headers=headers)
    print(response)
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f'Project {project_id} deleted successfully!')
        print(response.json())  # Optional: If the response contains data
        return True
    else:
        print(f'Failed to delete project. Status code: {response.status_code}')
        print(response.text)  # Print the error message
        return False

# Example usage