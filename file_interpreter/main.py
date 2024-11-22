import os
import json
import openai
from google.cloud import storage
from PyPDF2 import PdfReader
from openai import OpenAI
from ind_key import rand_k

# Configure your Google Cloud and OpenAI API credentials
sk = rand_k

def download_file_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from Google Cloud Storage."""
    if os.path.isfile(destination_file_name):
        return
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}")

def upload_file(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)


    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

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
        You can use the following class-description as an oriention {class_description}. Content:\n{chunk}"""
        
        response = client.chat.completions.create(
            model="gpt-4o",  # Oder ein anderes Modell wie "gpt-4"
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

def main():
    bucket_name = "raw_pdf_files"
    
    create_temp_folder()
    # Step 1: Download and read JSON files
    download_file_from_gcs(bucket_name, "json_files/labels_with_descriptions.json", "temp/classes.json")
    download_file_from_gcs(bucket_name, "json_files/classification.json", "temp/pdfs_with_classes.json")
    
    with open("classes.json", "r") as file:
        entities = json.load(file)
    
    with open("pdfs_with_classes.json", "r") as file:
        pdf_classes = json.load(file)
    
    # Step 2: Process each class
    for entity in entities:
        class_name = entity["name"]
        class_description = entity["description"]
        related_terms = entity["tokens"]
        
        # Select PDFs fitting the class
        fitting_pdfs = [
            pdf_info["title"]
            for pdf_info in pdf_classes
            if class_name in pdf_info["labels"]
        ]
        
        # Summarize each PDF and compile into a text file
        summaries = []
        for pdf_name in fitting_pdfs:
            local_pdf_path = f"temp/{pdf_name}"
            download_file_from_gcs(bucket_name, f"raw_pdf_files/{pdf_name}", local_pdf_path)
            summary = summarize_pdf_content(local_pdf_path, class_name, class_description, related_terms)
            print(f"Completed {pdf_name}")
            summaries.append(f"Summary for {pdf_name}:\n{summary}\n\n")
        
        # Save summaries to a text file
        with open(f"temp/{class_name}.txt", "w") as txt_file:
            txt_file.writelines(summaries)
        print(f"Summaries saved to {class_name}.txt")
        upload_file(bucket_name,f"temp/{class_name}.txt",f"summaries/{class_name}.txt")

if __name__ == "__main__":
    main()
