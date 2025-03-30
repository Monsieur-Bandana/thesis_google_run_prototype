import requests
from shared.ind_key import git
import os

url_def = "https://raw.githubusercontent.com/Monsieur-Bandana/thesis_google_run_prototype/refs/heads/structured_functions_test/labels_with_descriptions_structured.json"


def load_class_data_from_git(parent: str, url=url_def):
    """
    loads the EF-bluieprint file. The file is located on git, to ease edit and commit processes
    """
    local_filename = f"{parent}/temp/classes.json"
    token = git

    headers = {"Authorization": f"token {token}"}

    if not os.path.isfile(local_filename):

        try:

            response = requests.get(url, headers=headers)

            response.raise_for_status()

            with open(local_filename, "w", encoding="utf-8") as file:
                file.write(response.text)

            print(f"File downloaded successfully as {local_filename}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    else:
        print(f"{local_filename} already exists!")
