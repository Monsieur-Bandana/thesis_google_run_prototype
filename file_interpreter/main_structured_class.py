import json
import os
from PyPDF2 import PdfReader
from openai import OpenAI
# from ind_key import rand_k
from txt_generator import process_json_to_text
from json_processor import merge_json_information, create_json_file, check_file_got_already_interpreted
from shared.git_handler import load_class_data_from_git
from shared.gcs_handler import list_files_in_folder, download_file_from_bucket, upload_file, list_directories_in_bucket, create_temp_folder
from shared.ind_key import rand_k
from class_contructor import InterpreterStructure

# Configure your Google Cloud and OpenAI API credentials
sk = rand_k
main_folder = "file_interpreter"
prefix = 'raw_pdf_files/'
bucket_name = "raw_pdf_files"
labels_data = []
interpreted_files = []

def execute_summary(prompt, content, save_file, pdf_file_path, chunk_size, comp, dir):
    content_chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
    print(f"----------------------> amount of content = {len(content_chunks)}")

    client = OpenAI(api_key=sk)
    context_1 = f"""
                You are a helpful assistant tasked with extracting information about Smartphones and their environmental impact. \n

                """
    if not comp == "general":
        context_1 = f"""
                    You are a helpful assistant tasked with extracting information about {comp}-Smartphones, also referred to as {dir}-Smartphones and their environmental impact. \n
                    - Focus exclusively on information that directly pertains to {comp} and its products, such as the {comp}-Smartphone, as mentioned in the provided text. \n
                    - Ensure the name "{comp}" is explicitly mentioned in your response where relevant. \n
                    - Ignore general information about the smartphone industry unless it explicitly relates to {comp}. \n

                    """

    chunk_nr = 0
    for chunk in content_chunks:

        context_2 = f"""
                    Your responsibilities are as follows:\n
                    - Summarize key points in concise bullet points.\n
                    - Extract specific details, including important figures, data, and statistics, where available, while keeping the response concise.\n

                    **Important Instructions**:\n
                    - Use only the information provided in the following text as your source. Do not incorporate any external knowledge or assumptions.\n
                    - If no relevant information is found in the provided text, return following string (`"..."`) instead of attempting to answer the question.\n
                    - Format your response according to the given structure.\n

                    \n<text>{chunk}</text>\n

                    """
        context = context_1 + context_2

        element:dict = None
        print(f"----------->{pdf_file_path}-chunk-{chunk_nr}")
        for el in labels_data:
            if el["source"] == f"{os.path.basename(pdf_file_path)}-chunk-{chunk_nr}":
                element = el
                print("similarity found!")
                break
        valid_keys = []
        if element:

            valid_keys = element["list"]
        if valid_keys: 
            try:
                
                response = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",  # Oder ein anderes Modell wie "gpt-4"
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user", "content": prompt},
                    
                    ],
                    response_format=InterpreterStructure
                )

                summary = response.choices[0].message.content
                generated_answer_dict:dict = json.loads(summary)
                generated_answer_dict["source"]=f"{pdf_file_path}, chunk {chunk_nr}"

            

                # Step 4: Modify generated_answer_dict by removing entries whose keys are not in the valid list
                keys_to_remove = [key for key in generated_answer_dict if key not in valid_keys]
                
                # Remove the elements from generated_answer_dict
                for key in keys_to_remove:
                    del generated_answer_dict[key]         
                
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
            
        chunk_nr = chunk_nr + 1

def summarize_all_fitting_pdfs(prompt, pdf_list, save_file, comp, dir):
    """Summarizes all fitting pdfs and creates a json file"""
    for pdf_file_path in pdf_list:
        print(pdf_file_path)
        reader = PdfReader(pdf_file_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        
        chunk_size = 100000  # Adjust chunk size to stay within token limits

        
        execute_summary(prompt, content, save_file, pdf_file_path, chunk_size, comp, dir)
        global interpreted_files
        interpreted_files.append(pdf_file_path)

def checkForInterpreteFiles():
    file_n = "already_interpreted_files.json"
    download_file_from_bucket("raw_pdf_files", f"json_files/{file_n}", f"{main_folder}/temp/{file_n}")
    try:
        with open(f"{main_folder}/temp/{file_n}", "r") as file:
            global interpreted_files
            interpreted_files = json.load(file)
    except:
        print("no interpreted entries yet!")
        

def main():

    pdf_class_file = f"{main_folder}/temp/docs_with_labels.json"
    download_file_from_bucket("raw_pdf_files", "json_files/docs_with_labels.json", pdf_class_file)
    global labels_data
    with open(pdf_class_file, 'r') as file:
        labels_data = json.load(file)

    # TODO adapt to folder structure
    brandlist = list_directories_in_bucket(bucket_name, prefix)
    entities = []
        

    comps = []
    with open(f"{main_folder}/prefilter.json", "r") as file:
        comps = json.load(file)

    # get dirs, loop the following through dirs
    dirs = brandlist
    for dir in dirs:
        comp = ""
        for li_el in comps:
            if dir == li_el["product"]:
                comp = li_el["company"]
        list_of_files = list_files_in_folder(bucket_name, f"{prefix}{dir}")
        files_to_intperprete = []
        for file_ in list_of_files:
            filen = f"{main_folder}/temp/{file_.split("/")[2]}"
            download_file_from_bucket(bucket_name, file_, filen)
            files_to_intperprete.append(filen)
        print(files_to_intperprete)
        # Step 2: Process each class
        # TODO: test if it works
        load_class_data_from_git(main_folder)
        with open(f"{main_folder}/temp/classes.json", "r") as file:
            entities = json.load(file)
        question = "Provide a concise list of bullet points for each of the following topics related to smartphones and their environmental impact.\n"
        save_file = f"{main_folder}/temp/{dir}.json"
        for entity in entities:
            parent_children = entity["list"]
            fitting_pdfs: list[str] = files_to_intperprete
            
     
            for child in parent_children:
                class_name = child["name"]
                class_description: str = child["description"]
                related_terms = child["tokens"]
                question = f"""{question}\nTopic: {class_name} \n What is the status quo?
                In which ways does the smartphone's {class_name} impacts the smartphone's environmental footprint? What characterizes a smartphone's {class_name}?
                Further: {class_description} """
                if not dir == "general":
                    question+=f"does the {comp} mentions any methods on {class_name}?"
        print(question)

        fitting_pdfs = [item for item in fitting_pdfs if item not in interpreted_files]
        summarize_all_fitting_pdfs(question, fitting_pdfs, save_file, comp, dir)



                

                

if __name__ == "__main__":
    create_temp_folder(main_folder)
    checkForInterpreteFiles()
    main()
    brandlist = list_directories_in_bucket(bucket_name, prefix)

    with open(f"{main_folder}/temp/classes.json", "r") as file:
        entities = json.load(file)
    for brand in brandlist:
        dir = brand
        try:
            save_file = f"{main_folder}/temp/{dir}.json"
            with open(save_file, "r") as file:
                data:list[dict] = json.load(file)
            merged_dict:dict = {}
            for d in data:
                for key, value in d.items():
                    if key in merged_dict:
                        merged_dict[key] += value
                    else:
                        merged_dict[key] = value
            print(merged_dict)
            for key, value in merged_dict.items():
                s_file_n = f"file_interpreter/temp/{brand}-{key}.txt"
                with open(s_file_n, "w", encoding="utf-8") as file:
                    file.write(value)
                upload_file("raw_pdf_files", s_file_n, f"summaries_struct_c/{brand}-{key}.txt")
        except:
            print(f"file '{save_file}' does not exist")

    file_n = "already_interpreted_files.json"
    with open(f"{main_folder}/temp/{file_n}", "w") as file:
        json.dump(interpreted_files, file, indent=4)
    upload_file("raw_pdf_files", f"{main_folder}/temp/{file_n}", f"json_files/{file_n}")
