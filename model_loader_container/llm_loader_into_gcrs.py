## draw model from hugginface

from transformers import AutoModelForCausalLM, AutoTokenizer
from google.cloud import storage

import os

model_name = 'distilbert/distilgpt2'  # Replace with the specific model name
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

save_directory = './saved_model_directory2'  # Specify your desired directory
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

## add model to gcs


print("Current working directory:", os.getcwd())

def upload_file(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

bucket_name = "saved_directory2"
source_directory = "./saved_model_directory2"

destination_blob_name = "examplefile.md"  # Path in the bucket
for filename in os.listdir(source_directory):
    file_path = os.path.join(source_directory, filename)
    if os.path.isfile(file_path):  # Ensure it's a file, not a directory
        print(f"Processing file: {file_path}")
        upload_file(bucket_name, file_path, filename)