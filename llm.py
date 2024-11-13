from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
# Modell- und Tokenizer laden

# Eingabetext
def generateAnswer(input: str, model, tokenizer)  -> str:
    
    model = model
    tokenizer = tokenizer
    text = input

    # Tokenisierung des Eingabetexts
    inputs = tokenizer(text, return_tensors="pt")

    # Modell generiert Vorhersagen
    outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)

    # Generierten Text dekodieren
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(generated_text)

    return generated_text
