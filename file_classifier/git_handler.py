import requests

def load_class_data_from_git():
    # URL to the raw JSON file in the GitHub repository
    url = "https://raw.githubusercontent.com/Monsieur-Bandana/thesis_google_run_prototype/refs/heads/main/labels_with_descriptions.json"

    # Local filename to save the downloaded JSON file
    local_filename = "temp/classes.json"
    token = ""

    headers = {
        "Authorization": f"token {token}"
    }

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Write the content of the response to a file
        with open(local_filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        
        print(f"File downloaded successfully as {local_filename}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
