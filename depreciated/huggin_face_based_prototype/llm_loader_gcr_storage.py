from google.cloud import storage

import os

print("Current working directory:", os.getcwd())

# Replace with your bucket name
bucket_name = "saved_model_directory"

def list_files_in_folder(bucket_name):
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

# List files in bucket
print("Files in bucket:")
for filename in list_files_in_folder(bucket_name):
    print(filename)

# Upload a file to the bucket
source_file_name = "examplefile.md"  # Path to your local file
destination_blob_name = "examplefile.md"  # Path in the bucket
upload_file(bucket_name, source_file_name, destination_blob_name)
