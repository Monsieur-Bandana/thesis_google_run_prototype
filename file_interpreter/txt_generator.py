import json
import os

mainf = "file_interpreter"

collection_of_ignore_terms = ["are not detailed", "The text does not", "is not addressed in the text", "not outlined in the text"]

def process_json_to_text(json_file_path, classes, brandn, file_n_opt="struct") -> bool:
    """
    - transforms json file in txt summaries
    - returns True if it successfull. The bool value is important to allow parent-process to skip the following steps, if json file doesnt exists
    """

    # Open and load the JSON file
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of elements.")

        # Collect all keys in the first element
        all_keys = classes
        print(f"classes: {classes}")

        for key_ in all_keys:
            collected_strings = []
            key: str = key_["json_name"]
            file_n: str = key_["name"]

            # Collect string values from all elements for the current key
            for element in data:
                if key in element and isinstance(element[key], str):
                    var_text: str = element[key]
                    for ig_t in collection_of_ignore_terms:
                        if ig_t in var_text:
                            var_text = ""
                    collected_strings.append(var_text)
                else:
                    collected_strings.append('')  # Handle missing or non-string values

            # Merge collected strings
            merged_string = '\n\n'.join(collected_strings)

            # Save the merged string into a text file named after the key
            output_file_path = f"{mainf}/temp/{brandn}-{file_n}-{file_n_opt}.txt"
            with open(output_file_path, 'w') as output_file:
                output_file.write(merged_string)

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

"""
# Example usage
if __name__ == "__main__":
    brand = "huawei"
    json_file = f"{mainf}{brand}-Materials.json-merged.json"
    classes = ["metals", "chemicals", "alternatives", "origin", "source"]
    process_json_to_text(json_file, classes, brand)
"""

