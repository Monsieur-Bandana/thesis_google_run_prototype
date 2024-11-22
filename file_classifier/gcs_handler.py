from google.cloud import storage
import pdfplumber
import os
# from classifier import exec_file

print("Current working directory:", os.getcwd())

def list_files_in_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()  # List all files in the bucket
    return [blob.name for blob in blobs]

def list_files_in_folder(bucket_name, folder_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    if not folder_name.endswith('/'):
        folder_name += '/'

    blobs = bucket.list_blobs(prefix=folder_name) 
    return [blob.name for blob in blobs if not blob.name.endswith('/')]

def upload_file(bucket_name, source_file_name, destination_blob_name, folder_name=None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    if folder_name:
        if not folder_name.endswith('/'):
            folder_name += '/'
        destination_blob_name = folder_name + destination_blob_name

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def download_file_from_bucket(bucket_name, source_blob_name, destination_file_name, folder_name=None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    if folder_name:
        if not folder_name.endswith('/'):
            folder_name += '/'
        source_blob_name = folder_name + source_blob_name

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}")



    