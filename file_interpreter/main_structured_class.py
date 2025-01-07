import os
import json
import openai
from google.cloud import storage
from PyPDF2 import PdfReader
from openai import OpenAI
# from ind_key import rand_k
from txt_generator import process_json_to_text
from json_processor import merge_json_information, create_json_file, check_file_got_already_interpreted
from shared.git_handler import load_class_data_from_git
from shared.gcs_handler import list_files_in_folder, download_file_from_bucket, upload_file, list_directories_in_bucket, create_temp_folder
from shared.ind_key import rand_k
from class_contructor import class_list, InterpreterStructure

# Configure your Google Cloud and OpenAI API credentials
sk = rand_k
main_folder = "file_interpreter"
prefix = 'raw_pdf_files/'
bucket_name = "raw_pdf_files"

def execute_summary(prompt, content, save_file, pdf_file_path, chunk_size):
    content_chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
    print(f"----------------------> amount of content = {len(content_chunks)}")

    client = OpenAI(api_key=sk)


    chunk_nr = 0
    for chunk in content_chunks:
        try:
            chunk_nr = chunk_nr + 1
            prompt = prompt + f" Extract you information from the following text: {chunk} Convert your response into the given structure."
            
            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",  # Oder ein anderes Modell wie "gpt-4"
                messages=[
                    {"role": "user", "content": prompt},
                
                ],
                temperature=1,
                response_format=InterpreterStructure
            )

            summary = response.choices[0].message.content
            generated_answer_dict:dict = json.loads(summary)
            generated_answer_dict["source"]=f"{pdf_file_path}, chunk {chunk_nr}"
            create_json_file(generated_answer_dict, main_folder, save_file)
        except:
            """
            chunk_size = chunk_size - 1000
            if chunk_size < 90000: 
                print("smth went wrong")
                return
            print(f"{chunk[:1000]} \n \n {chunk[-1000:]}")
            execute_summary(prompt, content, save_file, index, pdf_file_path, chunk_size)
            """
            print(f"Chunk {chunk_nr} of {pdf_file_path} could not be interpreted") 

def summarize_all_fitting_pdfs(prompt, pdf_list, save_file):
    """Summarizes all fitting pdfs and creates a json file"""
    for pdf_file_path in pdf_list:
        print(pdf_file_path)
        reader = PdfReader(pdf_file_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        
        chunk_size = 100000  # Adjust chunk size to stay within token limits

        
        execute_summary(prompt, content, save_file, pdf_file_path, chunk_size)
        
def main():
    # TODO adapt to folder structure
    brandlist = list_directories_in_bucket(bucket_name, prefix)
    entities = []
        
    create_temp_folder(main_folder)



    # get dirs, loop the following through dirs
    dirs = brandlist
    for dir in dirs:
        list_of_files = list_files_in_folder(bucket_name, f"{prefix}{dir}")
        files_to_intperprete = []
        for file_ in list_of_files:
            filen = f"{main_folder}/temp/{file_.split("/")[2]}"
            download_file_from_bucket(bucket_name, file_, filen)
            files_to_intperprete.append(filen)
        print(files_to_intperprete)
        # Step 2: Process each class
        with open(f"{main_folder}/labels_with_descriptions_structured.json", "r") as file:
            entities = json.load(file)
        prompt = ""
        save_file = f"{main_folder}/temp/{dir}.json"
        for entity in entities:
            parent_children = entity["list"]
            fitting_pdfs: list[str] = files_to_intperprete
            
     
            for child in parent_children:
                class_name = child["name"]
                class_description = child["description"]
                related_terms = child["tokens"]

                prompt = prompt + f"""Extract all information about '{class_name}' within {dir}-company and summarize them in bullet points.
                You can use the following class-description as an oriention {class_description}. Also you can use the related terms: {', '.join(related_terms)} for
                better understanding of the topic.
                """
        print(prompt)
        summarize_all_fitting_pdfs(prompt, fitting_pdfs, save_file)



                

                

if __name__ == "__main__":
    # main()
    brandlist = list_directories_in_bucket(bucket_name, prefix)
    with open(f"{main_folder}/labels_with_descriptions_structured.json", "r") as file:
        entities = json.load(file)
    for brand in brandlist:
        dir = brand
        save_file = f"{main_folder}/temp/{dir}.json"
        with open(save_file, "r") as file:
            data = json.load(file)
        for entity in entities:
            json_file_n = f"{main_folder}/temp/{dir}-{entity["json_name"]}.json"
            parent_children = entity["list"]
            new_l = []
            print(f"ent____________ {entity}")
            for el_ in data:
                new_l.append(el_[entity["json_name"]])
            with open(json_file_n, "w") as file:
                json.dump(new_l, file, indent=4)

            
            json_exists: bool = process_json_to_text(json_file_n, parent_children, dir, "struct_class")
            if json_exists:
                for ch in parent_children:
                    output_file_path = f"""{main_folder}/temp/{dir}-{ch["name"]}-struct_class.txt"""
                    upload_file(bucket_name,output_file_path,f"summaries_struct_c/{dir}-{ch["name"]}.txt")