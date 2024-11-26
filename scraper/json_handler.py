import json
import os

def createJsonFromList(list, filename):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Specify the file name
    file_name = f'temp/{filename}.json'

    # Save the list as a JSON file
    with open(file_name, 'w') as json_file:
        json.dump(list, json_file)

    print(f"The list has been saved to {file_name}")

def cleanUpText(long_text, start, end) -> str:
    
    # Find the start and end indices
    start_index = long_text.find(start)
    end_index = long_text.find(end)

    # Ensure the phrases are found
    if start_index != -1 and end_index != -1:
        # Remove the text between the phrases
        cleaned_text = long_text[:start_index] + long_text[end_index + len(end):]
    else:
        cleaned_text = long_text  # If phrases not found, keep original text

    # Replace "\n" with " "
    cleaned_text = cleaned_text.replace("\n", " ")

    return cleaned_text
