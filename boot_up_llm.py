from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

def boot_model() -> tuple:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    load_directory = os.path.join(current_dir, 'saved_model_directory')
    
    model = AutoModelForCausalLM.from_pretrained(load_directory)
    tokenizer = AutoTokenizer.from_pretrained(load_directory)
    return model, tokenizer