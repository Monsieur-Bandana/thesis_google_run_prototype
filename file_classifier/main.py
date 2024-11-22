from llama_index.core import SimpleDirectoryReader
import json
import os
from pdf_handler import create_pdf_temp_folder
from gcs_handler import upload_file, download_file_from_bucket

classes = []
tokens = []
bucket_name = "raw_pdf_files"

def extract_classes():
    download_file_from_bucket(bucket_name, "json_files/labels_with_descriptions.json", "labels_with_descriptions.json")
    with open('labels_with_descriptions.json', 'r') as file:
        data: list = json.load(file)

        for el in data:
            classes.append(el["name"])
            tokens.append(el["tokens"])

def classify_text_using_retriever()->list[dict]:
    """
    * exec retriever for each label
    * outcome for each lebel stored in list.
    * if list empty label not in use
    """
    if not classes:
        extract_classes()
    
    pdf_docs = create_pdf_temp_folder(bucket_name)

    pdf_list = [os.path.basename(file) for file in os.listdir(pdf_docs)]

    reader = SimpleDirectoryReader(input_dir=pdf_docs, recursive=True,)
    collection:list[dict] = []
    i:int = 0
    for docs in reader.iter_data():
        title:str = os.path.basename(pdf_list[i])
        label_list = []
        x: int = 0
        for cl in classes:
            tokens_list = tokens[x]
            for doc in docs:

                if cl in doc.text and cl not in label_list:
                    
                    label_list.append(cl)
                for token in tokens_list:
                    if token in doc.text and cl not in label_list:
                        label_list.append(cl)
            x = x+1

            
        collection.append({"title": title, "labels": label_list})
        i = i+1
    
    # clear_temp_folder()
    return collection


list_of_dicts: list[dict] = classify_text_using_retriever()

output_file = "classification.json"

# Write the list of dictionaries to a JSON file
with open(output_file, "w") as file:
    json.dump(list_of_dicts, file, indent=4)

# bucket_name, source_file_name, destination_blob_name, folder_name=None
upload_file(bucket_name, "classification.json","classification.json", "json_files")
