from llama_index.core import SimpleDirectoryReader
import json
from pdf_extractor import create_pdf_temp_folder, clear_temp_folder

classes = []
descriptors = []

def extract_classes():
    with open('labels_with_descriptions.json', 'r') as file:
        data: list = json.load(file)

        for el in data:
            classes.append(el["name"])
            descriptors.append(el["description"])

def classify_text_using_retriever()->list:
    """
    * exec retriever for each label
    * outcome for each lebel stored in list.
    * if list empty label not in use
    """
    if not classes:
        extract_classes()
    bucket_name = "raw_pdf_files"
    docs = create_pdf_temp_folder(bucket_name)
    reader = SimpleDirectoryReader(input_dir=docs, recursive=True,)
    collection:list = []
    for docs in reader.iter_data():
        title:str = docs[0].text[:60]
        label_list = [title]
        for cl in classes:
            for doc in docs:
                # do stuff
            # Process only if the desired word appears in the document
                if cl in doc.text and cl not in label_list:
                    
                    label_list.append(cl)

            
        collection.append(label_list)
    
    # clear_temp_folder()
    return collection


print(str(classify_text_using_retriever()))    