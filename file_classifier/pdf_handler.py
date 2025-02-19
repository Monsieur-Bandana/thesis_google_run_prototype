from google.cloud import storage
import pdfplumber
import os
from shared.gcs_handler import download_file_from_bucket, list_files_in_folder

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text = text.encode('ascii', 'ignore').decode('utf-8')
            
    return text
"""
def process_pdfs_from_bucket_using_gpt(bucket_name):
    temp_folder = "temp_pdfs"
    os.makedirs(temp_folder, exist_ok=True)  # Ensure temp folder exists

    files_list = list_files_in_folder(bucket_name, "raw_pdf_files")
    for file_name in files_list:
        local_pdf_path = os.path.join(temp_folder, file_name)

        # Download file from GCS
        download_file_from_bucket(bucket_name, file_name, local_pdf_path, "raw_pdf_files")
        # Clean up local file
        os.remove(local_pdf_path)
"""

def create_pdf_temp_folder(bucket_name, parent, dir) -> str:
    temp_folder = f"{parent}/temp/{dir}"
    os.makedirs(temp_folder, exist_ok=True)  # Ensure temp folder exists

    files_list = list_files_in_folder(bucket_name, f"raw_pdf_files/{dir}")
    for file_name in files_list:
        local_pdf_path = os.path.basename(os.path.join(temp_folder, file_name))
        download_file_from_bucket(bucket_name, file_name, f"{temp_folder}/{dir}/{local_pdf_path}")

    return temp_folder

def clear_temp_folder():
    os.remove("temp_pdfs")