import os
import json



def merge_json(dict1, dict2):
    """
    Merge two dictionaries. If keys are the same:
      - Combine values if they are both dictionaries.
      - Create a list if they are non-dict values and not already lists.
      - Append to the list if one key already holds a list.
    """
    merged = dict1.copy()  # Start with the first dictionary
    
    for key, value in dict2.items():
        if key in merged:
            # If both values are dictionaries, merge them recursively
            if isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = merge_json(merged[key], value)
            # If value is a list or already merged into a list
            elif isinstance(merged[key], list):
                merged[key].append(value)
            elif isinstance(value, list):
                merged[key] = [merged[key]] + value
            else:
                # Otherwise, combine string
                merged[key] = merged[key] + value
        else:
            merged[key] = value
    
    return merged

def merge_json_information(main_folder = "file_interpreter",
file_path = "file_interpreter/test_on_materials-2.json"):
    data = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            data = json.load(file)
            if len(data) == 1: return
        comp_file_name = data[0]["source"].split(",")[0]
        comp_file = (comp_file_name, 0)
        new_edit: list[dict] = []
        index = 1
        for el in data[1:]:
            if el["source"].split(",")[0] == comp_file[0]:
                new_el:dict = merge_json(data[comp_file[1]], el)
                if new_edit:
                    new_edit.pop()
                new_edit.append(new_el)
            else:
                new_edit.append(el)
            comp_file_name = el["source"].split(",")[0]
            comp_file = (comp_file_name, index)
            index = index + 1
        with open(f"{file_path.split(".")[0]}-merged.json", "w") as file:
            json.dump(new_edit, file, indent=4)


def create_json_file(generated_answer_dict, main_folder, file_path):
    # Read existing content or initialize an empty list
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("The JSON file does not contain a list.")
            except json.JSONDecodeError:
                try: 
                    el = json.load(file)
                    if not isinstance(data, dict):
                        raise ValueError("The JSON file does not contain a dict.")
                    data[el]
                except:
                    data = []  # Initialize an empty list if file is empty or invalid

    else:
        data = []

    # Append the new dictionary
    data.append(generated_answer_dict)

    # Write the updated list back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def check_file_got_already_interpreted(check_for_file: str, check_for_json: str, classn: str) -> bool:
    """
    Check if a JSON file exists and contains a list, and verify if `check_for_file` 
    appears within the `source` characteristic of any item in the list.

    Args:
        check_for_file (str): The string to check for within the `source` characteristic.
        check_for_json (str): The path to the JSON file to check.

    Returns:
        bool: True if `check_for_file` appears in any `source`, False otherwise.
    """
    # Check if the JSON file exists
    if not os.path.isfile(check_for_json):
        return False

    # Read the JSON file
    try:
        with open(check_for_json, 'r') as file:
            data = json.load(file)

        # Ensure the file contains a list
        if not isinstance(data, list):
            return False

        # Loop through the list and check for the `source` characteristic
        for item in data:
            if isinstance(item, dict) and 'source' in item:
                if check_for_file in item['source']:
                    print(f"{check_for_file} alraedy got intepreted concerning {classn}")
                    return True

    except (json.JSONDecodeError, IOError):
        # Handle invalid JSON or file read errors
        return False

    # If no match is found, return False
    return False


