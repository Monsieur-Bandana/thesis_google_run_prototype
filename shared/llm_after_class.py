"""
TODO: allow multiple entities
"""
from openai import OpenAI
from shared.ind_key import rand_k
import os
import json
from google.cloud import storage
from google.api_core.exceptions import NotFound
from shared.gcs_handler import download_file_from_bucket
from shared.git_handler import load_class_data_from_git
import random

sk = rand_k
client = OpenAI(api_key=sk)

def replace_sentence_start(sentence: str, input, html_start):
    # List of typical sentence starting phrases
    starting_phrases = [
        "Further the phone",
        "Additionally it",
        "In addition the smartphone"
    ]
    
    # Check if the sentence starts with "The HUAWEI Pura 70 Ultra"
    if sentence.startswith(f"{html_start}The {input}"):
        # Replace the starting phrase with a randomly chosen phrase from the list
        return html_start + random.choice(starting_phrases) + sentence[len(f"{html_start}The {input}"):]
    
    # Return the original sentence if no match
    return sentence

# from ind_key import key
def give_conlusion(previous_text:str, class_name, phone_name)->str:
    context = f"""
    You are a helpful assistant, giving conlusions about the {class_name} related to smartphones.
    You only refer to the as-is situation and don't give any comments on how the footprint could potentially be improved.
    The review consists of a description of the as-is situation as well as it's impact on the environmental footprint.
    use exclusively the text between the <input> brackets as a source of information. <input> {previous_text} </input>.
    Keep the answer informative but brief. The length of the response should be kept arround 50 tokens.

    """

    question = f"""Give a brief summary about the carbon footprint of the {phone_name}. 
    Please mention in you summary wether the phone might have a good footprint or a rather bad one"""
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=200
    )
    
    generated_text = completion.choices[0].message.content

    return generated_text

# Eingabetext
def activate_api(input: str, class_name: str, rag_inf: str, fewshots: list[str], startsuggestion)  -> str:
    
    
    question:str = f"""Tell me about {class_name} of the {input}."""
    fewshot_question:str = f"""Tell me about {class_name} of the Luminara-phone."""
    comment = f""" Give the responses in the style of the following examples: Question: {fewshot_question} Answer: {fewshots[0]} Question: {fewshot_question} Answer: {fewshots[1]}"""

    context = f"""You are a helpful assistant, giving reviews about {class_name} related to smartphones.
    The review consists of a description of the as-is situation as well as it's impact on the environmental footprint.
    You only refer to the as-is situation and don't give any comments on how the footprint could potentially be improved.
    use exclusively the text between the <input> brackets as a source of information. <input> {rag_inf} </input>.
    Keep the answer informative but brief. The length of the response should be kept arround 50 tokens.
    """
    sk = rand_k
    client = OpenAI(api_key=sk)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=200
    )

    generated_text = completion.choices[0].message.content

    html_output = ''.join(f'{line} ' for line in generated_text.split('\n') if line.strip())

    return f"<li>{html_output}</li>"

def create_temp_folder(sourcefolder):
    folder_path = f"{sourcefolder}/temp"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def getContext(dir, class_name, sourcefolder):
    local_file_path = f"{sourcefolder}/temp/{dir}-{class_name}.txt"
    try:
        with open(local_file_path, 'r', encoding='utf-8') as file:
            print(f"extracted text from {local_file_path}")
            context = file.read()
    except UnicodeDecodeError:
        with open(local_file_path, 'r', encoding='ISO-8859-1') as file:
            context = file.read()
    return context

def get_element_by_name(file_path, input_name):
    try:
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data:list[dict] = json.load(file)

        # Iterate over the list of entities in the JSON
        for entity in data:
            if entity.get("name") == input_name:
                return entity.get("specs", "specs not found for this entity")

        return f"No entity found with the name '{input_name}'."
    except FileNotFoundError:
        return f"The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return "Error decoding JSON. Please check the file format."

def generateAnswer(input: str, sourcefolder):
    bucket_name = "raw_pdf_files"

    dir = "general"

    for brand in ["iphone", "fairphone", "huawei", "mi"]:
        if brand in input.lower():
            print(f"{brand} found in request {input.lower()}")
            dir = brand
            download_file_from_bucket(bucket_name, f"json_files/scraped-{dir}-data.json", f"{sourcefolder}/temp/scraped-{dir}-data.json")
        else: print(f"{brand} not found in request {input}")

    # extract model specific information

    
    create_temp_folder(sourcefolder)
    # Step 1: Download and read JSON files
    load_class_data_from_git(sourcefolder)
    
    with open(f"{sourcefolder}/temp/classes.json", "r") as file:
        entities = json.load(file)

    parenttitle = ""
    responses = []
    # Step 2: Process each class
    for entity in entities:
        class_name = entity["name"]
        

        context = ""
        try:
            download_file_from_bucket(bucket_name, f"summaries/{dir}-{class_name}.txt", f"{sourcefolder}/temp/{dir}-{class_name}.txt")
            context = getContext(dir, class_name, sourcefolder)
        except NotFound:
            print(f"file summaries/{dir}-{class_name}.txt not found")



        if not dir == "general":
            try:
                download_file_from_bucket(bucket_name, f"summaries/general-{class_name}.txt", f"{sourcefolder}/temp/general-{class_name}.txt")
                context = get_element_by_name(f"{sourcefolder}/temp/scraped-{dir}-data.json", input) + context + getContext("general", class_name, sourcefolder) 
            except NotFound:
                print(f"file summaries/general-{class_name}.txt not found")
        with open(f"{sourcefolder}/temp/{class_name}.txt", "w", encoding="utf-8") as file:
            file.write(context)
        
        # Summarize each PDF and compile into a text file
        response = ""
        
        if context.strip():
            fewshots = ["", ""] if entity.get("fewshots") is None else entity["fewshots"]
            startsuggestion = "" if entity.get("sug") is None else entity["sug"]
            response = activate_api(input, class_name, context, fewshots, startsuggestion)
            if not entity["parent"] == parenttitle:
                parenttitle = entity["parent"]
                responses.append(f'</ul><p>{parenttitle}</p><ul>')
            else:
                response = replace_sentence_start(response, input, "<li>")
            # responses.append(f"""<h2>{entity["name"]}</h2>{response}""")
            responses.append(response)
           
    final_resp = " ".join(responses)
    
    final_resp = final_resp[len("</ul>"):]
    final_resp = f"<p>{give_conlusion(final_resp, entity["name"], input)}</p><p>Further Details:</p>{final_resp}</ul>"
    return final_resp



## Testsection
# print(generateAnswer("HUAWEI nova 12i"))