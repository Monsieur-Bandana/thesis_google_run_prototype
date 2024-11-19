from google.cloud import storage
import pdfplumber
import os
from classifier import exec_file

print("Current working directory:", os.getcwd())

def list_files_in_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()  # List all files in the bucket
    return [blob.name for blob in blobs]

def upload_file(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text = text.encode('ascii', 'ignore').decode('utf-8')
            
    return text

def download_file_from_bucket(bucket_name, source_blob_name, destination_file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}")

def process_pdfs_from_bucket_using_gpt(bucket_name):
    temp_folder = "temp_pdfs"
    os.makedirs(temp_folder, exist_ok=True)  # Ensure temp folder exists

    files_list = list_files_in_bucket(bucket_name)
    for file_name in files_list:
        local_pdf_path = os.path.join(temp_folder, file_name)

        # Download file from GCS
        download_file_from_bucket(bucket_name, file_name, local_pdf_path)

        # Extract text from PDF
        try:
            pdf_text = extract_text_from_pdf(local_pdf_path)
            exec_file(pdf_text)
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

        # Clean up local file
        os.remove(local_pdf_path)

def create_pdf_temp_folder(bucket_name) -> str:
    temp_folder = "temp_pdfs"
    os.makedirs(temp_folder, exist_ok=True)  # Ensure temp folder exists

    files_list = list_files_in_bucket(bucket_name)
    for file_name in files_list:
        local_pdf_path = os.path.join(temp_folder, file_name)
        download_file_from_bucket(bucket_name, file_name, local_pdf_path)

    return temp_folder

def clear_temp_folder():
    os.remove("temp_pdfs")


    