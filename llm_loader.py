from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = 'Writer/palmyra-small'  # Replace with the specific model name
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

save_directory = './saved_model_directory'  # Specify your desired directory
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
