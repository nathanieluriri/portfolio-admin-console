import requests
import json

def exclude_none(data):
    return {key: value for key, value in data.items() if value is not None}

def update_project_func(base_url,project_id,name=None,description=None,image_link=None,case_study_link=None):
    url = f"{base_url}/update/project/{project_id}"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    data = {
          "name": name,
  "description": description,
  "case_study_image_link": image_link,
  "case_study_link": case_study_link
}
    
    data = exclude_none(data=data)

    # Make the PATCH request
    response = requests.patch(url, headers=headers, json=data)

    # Check the status of the request
    if response.status_code == 200:
        print("Project updated successfully!")
        return True # Return the response if needed
    else:
        print(f"Failed to update project: {response.status_code}")
        return response.text  # Return the error message or response text for debugging

# Call the function to update the project
