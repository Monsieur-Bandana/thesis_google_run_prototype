import os
import json
import openai
from google.cloud import storage
from PyPDF2 import PdfReader
from openai import OpenAI
# from ind_key import rand_k
from git_handler import load_class_data_from_git
from gcs_handler import list_files_in_folder, download_file_from_bucket, upload_file, list_directories_in_bucket

# Configure your Google Cloud and OpenAI API credentials
sk = ""

def summarize_pdf_content(pdf_file_path, focus_class, class_description, related_terms):
    """Summarizes the content of a PDF with focus on a class and related terms."""
    reader = PdfReader(pdf_file_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    
    chunk_size = 30000  # Adjust chunk size to stay within token limits
    content_chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    
    client = OpenAI(api_key=sk)
    
    summaries = []
    for chunk in content_chunks:
        prompt = f"""Summarize the following content with a focus on the class '{focus_class}' and related terms: {', '.join(related_terms)}.
        You can use the following class-description as an oriention {class_description}. Don't write complete sentences, prefer concluding texts in bullet points. Content:\n{chunk}"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Oder ein anderes Modell wie "gpt-4"
            messages=[
                {"role": "user", "content": prompt},
            
            ],
            temperature=1  # Geringere Temperatur für deterministischere Ergebnisse
        )

        summary = response.choices[0].message.content
        summaries.append(summary)
    return "\n".join(summaries)

def create_temp_folder():
    folder_path = "temp"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def get_existing_summaries(bucketname):
    files = list_files_in_folder(bucketname, "summaries")
    for file in files:
        filename = file.split("/")[1]
        download_file_from_bucket(bucketname, file, f"temp/{filename}")

def check_if_txt_file_already_exists(txt_path)->bool:
    if os.path.exists(txt_path):
        return True
    return False

def check_if_file_got_already_interpreted(txt_path, pdf_path)-> bool:
    # Specify the file path and the text line to search for
    
    search_text = pdf_path

    # Check if the file exists
    if os.path.exists(txt_path):
        print(f"{txt_path} exists")
        # Open the file and check for the line
        with open(txt_path, "r", encoding="utf-8") as file:
            for line in file:
                if search_text in line:
                    print(f"{search_text} exists in the file.")
                    return True
                else:
                    print(f"searching for {search_text} ...")
    
    return False
    


def main():
    # TODO adapt to folder structure
    prefix = 'raw_pdf_files/'
    bucket_name = "raw_pdf_files"
    brandlist = list_directories_in_bucket(bucket_name, prefix)
        
    create_temp_folder()
    get_existing_summaries(bucket_name)
    # Step 1: Download and read JSON files
    list_of_jsons = list_files_in_folder(bucket_name, "json_files")
    for file in list_of_jsons:
        filename = file.split("/")[1]
        if "classification" in filename:
            download_file_from_bucket(bucket_name, file, f"temp/{filename}")

    load_class_data_from_git()
    with open("temp/classes.json", "r") as file:
        entities = json.load(file)
    
    # get dirs, loop the following through dirs
    dirs = brandlist
    for dir in dirs:

        with open(f"temp/{dir}-classification.json", "r") as file:
            pdf_classes = json.load(file)
        
        # Step 2: Process each class
       
        for entity in entities:
            class_name = entity["name"]
            class_description = entity["description"]
            related_terms = entity["tokens"]
            
            
            # Select PDFs fitting the class
            fitting_pdfs = [
                f"""{dir}/{pdf_info["title"]}"""
                for pdf_info in pdf_classes
                if class_name in pdf_info["labels"]
            ]
            
            # Summarize each PDF and compile into a text file
            summaries = []
            for pdf_name in fitting_pdfs:
                if not check_if_file_got_already_interpreted(f"temp/{dir}-{class_name}.txt", f"""{dir}/{pdf_name.split("/")[1]}"""):
                    local_pdf_path = f"""temp/{pdf_name.split("/")[1]}"""
                    download_file_from_bucket(bucket_name, f"raw_pdf_files/{pdf_name}", local_pdf_path)
                    summary = summarize_pdf_content(local_pdf_path, class_name, class_description, related_terms)
                    print(f"Completed {pdf_name}")
                    summaries.append(f"Summary for {pdf_name}:\n{summary}\n\n")
            
            # Save summaries to a text file
            if summaries:
                if not check_if_txt_file_already_exists(f"temp/{dir}-{class_name}.txt"):
                    with open(f"temp/{dir}-{class_name}.txt", "w", encoding="utf-8") as txt_file:
                        txt_file.writelines(summaries)
                    print(f"Summaries saved to {class_name}.txt")
                else:
                    with open(f"temp/{dir}-{class_name}.txt", "a", encoding="utf-8") as txt_file:
                        txt_file.writelines(summaries)
                    print(f"Summaries added to {class_name}.txt")
                upload_file(bucket_name,f"temp/{dir}-{class_name}.txt",f"summaries/{dir}-{class_name}.txt")

if __name__ == "__main__":
    main()
