from llama_index.core import SimpleDirectoryReader
import json
import os
from pdf_handler import create_pdf_temp_folder

classes = []
tokens = []

def extract_classes():
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
    bucket_name = "raw_pdf_files"
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

output_file = "output.json"

# Write the list of dictionaries to a JSON file
with open(output_file, "w") as file:
    json.dump(list_of_dicts, file, indent=4)
