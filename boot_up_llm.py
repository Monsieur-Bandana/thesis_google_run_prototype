from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import os
from google.cloud import storage
from flask import Flask

def boot_model_llama() -> tuple:
    model = AutoModelForCausalLM.from_pretrained('nvidia/Llama-3.1-Nemotron-70B-Instruct-HF')
    tokenizer = AutoTokenizer.from_pretrained('nvidia/Llama-3.1-Nemotron-70B-Instruct-HF')
    return model, tokenizer

def boot_model() -> tuple:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    load_directory = os.path.join(current_dir, 'saved_model_directory2')

    model = AutoModelForCausalLM.from_pretrained(load_directory)
    tokenizer = AutoTokenizer.from_pretrained(load_directory)
    return model, tokenizer


def boot_model_from_gc() -> tuple:
    bucket_name = "saved_directory2"
    model_dir = ""
    local_model_dir = "saved_directory2"

    # Initialize GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Download all model files from GCS
    os.makedirs(local_model_dir, exist_ok=True)
    blobs = bucket.list_blobs(prefix=model_dir)

    for blob in blobs:
        # Construct local file path
        file_path = os.path.join(local_model_dir, blob.name[len(model_dir) + 0:])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Downloading {blob.name} to {file_path}")
        blob.download_to_filename(file_path)
        
    model = AutoModelForCausalLM.from_pretrained(local_model_dir)
    tokenizer = AutoTokenizer.from_pretrained(local_model_dir)
    return model, tokenizer