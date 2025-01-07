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
from class_contructor import class_list

# Configure your Google Cloud and OpenAI API credentials
sk = rand_k
main_folder = "file_interpreter"

def execute_summary(prompt, content, save_file, index, pdf_file_path, chunk_size):
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
                response_format=class_list[index]  # Geringere Temperatur für deterministischere Ergebnisse
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

def summarize_all_fitting_pdfs(prompt, pdf_list, save_file, index):
    """Summarizes all fitting pdfs and creates a json file"""
    for pdf_file_path in pdf_list:
        print(pdf_file_path)
        reader = PdfReader(pdf_file_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        
        chunk_size = 100000  # Adjust chunk size to stay within token limits

        
        execute_summary(prompt, content, save_file, index, pdf_file_path, chunk_size)
        
def main():
    # TODO adapt to folder structure
    prefix = 'raw_pdf_files/'
    bucket_name = "raw_pdf_files"
    brandlist = list_directories_in_bucket(bucket_name, prefix)
    entities = []
        
    create_temp_folder(main_folder)
    # Step 1: Download and read JSON files
    list_of_jsons = list_files_in_folder(bucket_name, "json_files")
    for file in list_of_jsons:
        filename = file.split("/")[1]
        if "classification" in filename:
            download_file_from_bucket(bucket_name, file, f"{main_folder}/temp/{filename}")

    # load_class_data_from_git(main_folder)
    with open(f"{main_folder}/labels_with_descriptions_structured.json", "r") as file:
        entities = json.load(file)
    # get dirs, loop the following through dirs
    dirs = brandlist
    for dir in dirs:

        with open(f"{main_folder}/temp/{dir}-classification.json", "r") as file:
            pdf_classes = json.load(file)
        
        # Step 2: Process each class
        class_index: int = 0
        for entity in entities:
            parent_name = entity["name"]
            parent_children = entity["list"]
            fitting_pdfs: list[str] = []
            
            prompt = ""
     
            save_file = f"{main_folder}/temp/{dir}-{parent_name}.json"
            for child in parent_children:
                class_name = child["name"]
                class_description = child["description"]
                related_terms = child["tokens"]
                
                for pdf_info in pdf_classes:
                    if class_name in pdf_info["labels"]:
                        file_to_check = f"""file_interpreter/temp/{pdf_info["title"]}"""
                        if not file_to_check in fitting_pdfs:
                # Select PDFs fitting the class
                            already_ex: bool = check_file_got_already_interpreted(file_to_check, save_file, parent_name)
                            if not already_ex:
                                fitting_pdfs.append(file_to_check)


                prompt = prompt + f"""Extract all information about '{class_name}' within {dir}-company and summarize them in bullet points.
                You can use the following class-description as an oriention {class_description}. Also you can use the related terms: {', '.join(related_terms)} for
                better understanding of the topic.
                """

            print(fitting_pdfs)
            summarize_all_fitting_pdfs(prompt, fitting_pdfs, save_file, class_index)
            class_index = class_index + 1
            
            # merge_json_information(file_path=file_path_for_json)
            # extract each class into a txt file
            json_exists: bool = process_json_to_text(save_file, parent_children, dir)
            if json_exists:
                for ch in parent_children:
                    output_file_path = f"""{main_folder}/temp/{dir}-{ch["name"]}-struct.txt"""
                    upload_file(bucket_name,output_file_path,f"summaries_struct_l/{dir}-{ch["name"]}.txt")


if __name__ == "__main__":
    main()
