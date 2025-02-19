from PyPDF2 import PdfReader
from llama_index.core import SimpleDirectoryReader
import json
import os
from classif_str import InterpreterFormatOnDominance
from shared.json_processor import create_json_file
from shared.git_handler import load_class_data_from_git
from pdf_handler import create_pdf_temp_folder
from shared.gcs_handler import upload_file, download_file_from_bucket, list_directories_in_bucket, create_temp_folder
from sources_handler import add_footnotes
from openai import OpenAI
from shared.ind_key import rand_k
import re

classes = []
tokens = []
bucket_name = "raw_pdf_files"
folder_name = "file_classifier"

def extract_classes():
    load_class_data_from_git(folder_name)
    with open(f'{folder_name}/temp/classes.json', 'r') as file:
        data: list = json.load(file)

        for el in data:
            classes.append(el["name"])
            tokens.append(el["tokens"])

def classify_text_using_retriever(dir: str, classes: list[str])->list[dict]:
    """
    * exec retriever for each label
    * outcome for each label stored in list.
    * if list empty label not in use
    """
    pdf_docs = create_pdf_temp_folder(bucket_name, folder_name, dir)
    chunk_size = 100000 


    pdf_list = [file for file in os.listdir(pdf_docs) if file.lower().endswith(".pdf")]
    print(pdf_list)



    reader = SimpleDirectoryReader(input_dir=pdf_docs, recursive=True,)
    collection:list[dict] = []
    i:int = 0
    with open(f"{folder_name}/temp/classes.json", "r") as file:
        classes = json.load(file)

    for pdf_file_path in pdf_list:
        reader = PdfReader(f"{folder_name}/temp/{dir}/{pdf_file_path}")
        content = ""
        for page in reader.pages:
            page_text = page.extract_text()
            lines = page_text.split("\n")
            
            for line in lines:
                if line.strip().lower() == "references":  # Prüft, ob "References" eine eigene Zeile ist
                    break  # Stoppe hier die Verarbeitung
                content += line + "\n"
            else:
                continue  # Falls nicht gebrochen wurde, nächste Seite laden
            break  # Falls "References" gefunden wurde, Abbruch

        with open(f"{folder_name}/temp/contents--{pdf_file_path[0:8]}.txt", "w", encoding="utf-8") as file:
            file.write(content)

        content_chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

        question = ""
        for cl in classes:
            question = f"""{question}\nTopic: {cl["name"]} \n Description: {cl["description"]} What is the status quo? what direct or indirect impact has it on the environment?"""
        if not dir == "general":
            question+=f"does the manufacturer of the {dir} mentions any methods to improve the {cl["name"]}?"
        # if dir how does company tries to improve?
        chunk_nr = 0
        answeres_list = []
        for content in content_chunks:
            chunk_nr = chunk_nr + 1
            
            sk = rand_k
            client = OpenAI(api_key=sk)

            context = f"""

                You are a helpful assistant. You will receive a long document and evaluate its relevance to specific topics.  

                ### **Evaluation Guidelines:**  
                - Carefully scan the entire document to check if **any section** contains information relevant to the topic.  
                - Assign a probability float value between **0 and 1** based on the most relevant section.  
                - **Do not base your score on the average relevance of the document. If a small but highly relevant section exists, score accordingly.**  

                ### **Scoring Criteria:**  
                - **1.0**: A section fully answers a question on the topic.  
                - **0.8**: A section provides strong hints or partial answers but is not exhaustive.  
                - **0.5**: Some relevant mentions exist, but they are vague or incomplete.  
                - **0.2**: The document briefly touches on the topic but lacks real value.  
                - **0.0**: No relevant information is present.  

                ### **Important Instructions:**  
                - **If even a small part of the document contains valuable information, base the score on that section, not the overall text.**  
                - **If a score below 0.5 is given, provide a short explanation of why the document is insufficient.**  

                ### **Example Evaluations:**  
                #### Example 1:  
                Document: 40 pages, one page discusses “Mitochondria” in detail.  
                Topic: Biology  
                Rating: **0.9**  

                #### Example 2:  
                Document: 40 pages, mitochondria are mentioned briefly in one sentence.  
                Topic: Biology  
                Rating: **0.3**  

                #### Example 3:  
                Document: 40 pages, no mention of mitochondria.  
                Topic: Biology  
                Rating: **0.0**  

                ### Reasoning
                please also add a view sentences why you dicided for that score

                Now, evaluate the following document:  
                {content}

            """

            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": context},
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=0.2,
                response_format=InterpreterFormatOnDominance
            )
            summary = response.choices[0].message.content
            generated_answer_dict:dict = json.loads(summary)
            answeres_list.append(generated_answer_dict)


        final_anser_dict = {"source": pdf_file_path, "answeres": answeres_list, "brand": dir}
            
        create_json_file(final_anser_dict, "file_classifier", f"{folder_name}/temp/save_file.json")
        i = i+1
    
    # clear_temp_folder()
    return collection

# for each directory in google cloud storage:
prefix = 'raw_pdf_files/'
directories = list_directories_in_bucket(bucket_name, prefix)
print(directories)

create_temp_folder(folder_name)

if not classes:
    extract_classes()

for directory in directories[:4]:


    text_classifications: list[dict] = classify_text_using_retriever(directory, classes)



with open(f"{folder_name}/temp/save_file.json", "r") as file:
    data = json.load(file)
outc_l:list[dict] = []
for el in data:
    class_list = []

    som_l:dict = el["answeres"]

    for el_dict in som_l:
        for key, el2 in el_dict.items():
            print(el2)
            print(key)
            if el2["probability"] >= 0.5:
                cl_name = key
                if key not in class_list:
                    class_list.append(key)

    create_json_file({"source": el["source"],"list": class_list, "brand": el["brand"]}, "file_classifier", f"{folder_name}/temp/save_file2.json")
    # bucket_name, source_file_name, destination_blob_name, folder_name=None
    # upload_file(bucket_name, f"{folder_name}/temp/{output_file}",output_file, "json_files")

add_footnotes(folder_name, classes)