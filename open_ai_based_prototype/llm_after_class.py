from openai import OpenAI
# from ind_key import rand_k
import os
import json
from google.cloud import storage
from google.api_core.exceptions import NotFound
# from ind_key import key

def accessScientificInformation() -> str:
    return ""
# Eingabetext
def activate_api(input: str, class_name: str, rag_inf: str)  -> str:
    
    rand_k = ""
    
    
    comment = f"""please tell me about {class_name} of the {input}"""

    context = f"""You are a helpful assistant, returning a structered text about {class_name} related to smartphones.
    use exclusively the text between the <input> brackets as a source of information. <input> {rag_inf} <input>."""
    sk = rand_k
    client = OpenAI(api_key=sk)
    
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": comment
            }
        ],
        max_tokens=200
    )
    
    generated_text = completion.choices[0].message.content
    html_output = ''.join(f'<p>{line}</p>' for line in generated_text.split('\n') if line.strip())

    return html_output

def create_temp_folder():
    folder_path = "temp"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def download_file_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from Google Cloud Storage."""
    if os.path.isfile(destination_file_name):
        return
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}")

def getContext(dir, class_name):
    local_file_path = f"temp/{dir}-{class_name}.txt"
    try:
        with open(local_file_path, 'r', encoding='utf-8') as file:
            print(f"extracted text from {local_file_path}")
            context = file.read()
    except UnicodeDecodeError:
        with open(local_file_path, 'r', encoding='ISO-8859-1') as file:
            context = file.read()
    return context

def get_element_by_name(file_path, input_name):
    try:
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data:list[dict] = json.load(file)

        # Iterate over the list of entities in the JSON
        for entity in data:
            if entity.get("name") == input_name:
                return entity.get("specs", "specs not found for this entity")

        return f"No entity found with the name '{input_name}'."
    except FileNotFoundError:
        return f"The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return "Error decoding JSON. Please check the file format."

def generateAnswer(input: str):
    bucket_name = "raw_pdf_files"

    dir = "general"

    for brand in ["iphone", "fairphone", "huawei"]:
        if brand in input.lower():
            print(f"{brand} found in request {input}")
            dir = brand
            download_file_from_gcs(bucket_name, f"json_files/scraped-{dir}-data.json", f"temp/scraped-{dir}-data.json")
        print(f"{brand} not found in request {input}")

    # extract model specific information

    
    create_temp_folder()
    # Step 1: Download and read JSON files
    download_file_from_gcs(bucket_name, "json_files/labels_with_descriptions.json", "temp/classes.json")
    
    with open("temp/classes.json", "r") as file:
        entities = json.load(file)

    responses = []
    # Step 2: Process each class
    for entity in entities:
        class_name = entity["name"]

        context = ""
        try:
            download_file_from_gcs(bucket_name, f"summaries/{dir}-{class_name}.txt", f"temp/{dir}-{class_name}.txt")
            context = getContext(dir, class_name)
        except NotFound:
            print(f"file summaries/{dir}-{class_name}.txt not found")



        if not dir == "general":
            try:
                download_file_from_gcs(bucket_name, f"summaries/general-{class_name}.txt", f"temp/general-{class_name}.txt")
                context = get_element_by_name(f"temp/scraped-{dir}-data.json", input) + context + getContext("general", class_name) 
            except NotFound:
                print(f"file summaries/general-{class_name}.txt not found")
        with open(f"temp/{class_name}.txt", "w", encoding="utf-8") as file:
            file.write(context)
        
        # Summarize each PDF and compile into a text file
        response = ""
       
        if context.strip():
            response = activate_api(input, class_name, context)
            resposne_with_title = f'<h1>{class_name}</h1>{response}'
            responses.append(resposne_with_title)

    return " ".join(responses)

## Testsection
print(generateAnswer("HUAWEI nova 12i"))