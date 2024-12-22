"""
TODO: allow multiple entities
"""
from openai import OpenAI
from shared.ind_key import rand_k
import os
import json
from google.cloud import storage
from google.api_core.exceptions import NotFound
from shared.gcs_handler import download_file_from_bucket, create_temp_folder
from shared.git_handler import load_class_data_from_git
from shared.test_center import conclusion_tester
import random
from pydantic import BaseModel

sk = rand_k
client = OpenAI(api_key=sk)

def replace_sentence_start(sentence:str, input):
    # List of typical sentence starting phrases
    starting_phrases = [
        "Further the phone",
        "Additionally it",
        "In addition the smartphone",
        "Moreover, the device",
        "Furthermore, it",
        "What's more, the smartphone",
        "To add to this, the phone",
        "On top of that, the device",
        "In a similar vein, the smartphone",
        "Not only that, but it",
        "Besides this, the phone",
        "Equally important, the device",
        "As an additional point, the smartphone",
        "To expand further, it",
        "Additionally, the device",
        "Building on this, the phone",
        "Supplementing this, the smartphone",
        "In continuation, it",
        "Another noteworthy point is that the phone",
        "Correspondingly, the smartphone",
        "In the same regard, it",
        "To elaborate, the device",
        "Extending this idea, the phone"
    ]
    
    # Check if the sentence starts with "The HUAWEI Pura 70 Ultra"
    if sentence.startswith(f"The {input}"):
        # Replace the starting phrase with a randomly chosen phrase from the list
        return random.choice(starting_phrases) + sentence[len(f"The {input}"):]
    
    # Return the original sentence if no match
    return sentence

# from ind_key import key
def give_conlusion(previous_text:str, class_name, phone_name, count)->str:
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
        max_tokens=200,
    )
    
    generated_text = completion.choices[0].message.content
    if conclusion_tester(generated_text):
        return generated_text
    elif count < 4: 
        count = count + 1
        return give_conlusion(previous_text, class_name, phone_name, count)
    else:
        return "An Error happened generating the summary"

class FromatWithAdjective(BaseModel):
    summary: str
    adjective: str

def activate_api(input: str, class_name: str, rag_inf: str, isParent, footnotes: list[int])  -> str:
    
    
    question: str = f"""Tell me about {class_name} of the {input}."""
    fewshot_question: str = f"""Tell me about {class_name} of the Luminara-phone."""
    # comment = f""" Give the responses in the style of the following examples: Question: {fewshot_question} Answer: {fewshots[0]} Question: {fewshot_question} Answer: {fewshots[1]}"""

    context = f"""You are a helpful assistant, giving reviews about {class_name} related to smartphones.
    The review consists of a description of the as-is situation and wether this benefits or increases it's impact on the environmental footprint.
    You only refer to the as-is situation and don't give any comments on how the footprint could potentially be improved.
    use exclusively the text between the <input> brackets as a source of information. <input> {rag_inf} </input>.
    Keep the answer informative but brief. The length of the response should be kept arround 50 tokens.
    Further create one or two adjective about the environmental impact according to your response.
    If you use two, add a fitting connector between, such as "and" or "but".
    Convert your response into the given structure.
    """
    sk = rand_k
    client = OpenAI(api_key=sk)
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=200,
        response_format=FromatWithAdjective
    )

    generated_answer:str = completion.choices[0].message.content
    generated_answer_dict:dict = json.loads(generated_answer)
    
    generated_text:str = generated_answer_dict["summary"]
    generated_adj:str = generated_answer_dict["adjective"]
    generated_adj = generated_adj.capitalize()

    if not isParent:
        generated_text = replace_sentence_start(generated_text, input)

    html_output = ''.join(f'{line} ' for line in generated_text.split('\n') if line.strip())

    footnotes.sort()
    footnotes_span: str = ', '.join(map(str, footnotes))

    return f"""<li class="{class_name}"><span style="font-weight: bold">{generated_adj} {class_name}:</span> {html_output}<span class="sources">{footnotes_span}</span></li>"""

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
    
def download_and_extract_json(file_name, sourcefolder)->list:
    download_file_from_bucket("raw_pdf_files", f"json_files/{file_name}.json", f"{sourcefolder}/temp/{file_name}.json")
    outc_list = []
    with open(f"{sourcefolder}/temp/{file_name}.json", "r") as file:
        outc_list = json.load(file)
    print(outc_list)
    return outc_list

def extract_footnotes(class_n, dir_, foot_note_list:list[dict])->list:
    outc_list: list[int] = []
    for el in foot_note_list:
        if el["name"] == class_n:
            footnotes: list[dict] = el["footnotes"]
            for fel in footnotes:
                if fel["category"] == dir_:
                    outc_list.append(fel["footnote"])
    return outc_list

def generateAnswer(input: str, sourcefolder):
    bucket_name = "raw_pdf_files"
    
    create_temp_folder(sourcefolder)
    brandlist: list[str] = download_and_extract_json("all_companies", sourcefolder)
    foot_note_list: list[dict] = download_and_extract_json("footnotes", sourcefolder)

    print(foot_note_list)

    brandlist.append("general")

    dir = "general"
    # TODO load data from scraped company json
    for brand in brandlist:
        if brand in input.lower():
            print(f"{brand} found in request {input.lower()}")
            dir = brand
            download_file_from_bucket(bucket_name, f"json_files/scraped-{dir}-data.json", f"{sourcefolder}/temp/scraped-{dir}-data.json")
        else: print(f"{brand} not found in request {input}")

    # extract model specific information

    
    # Step 1: Download and read JSON files
    load_class_data_from_git(sourcefolder)
    
    with open(f"{sourcefolder}/temp/classes.json", "r") as file:
        entities = json.load(file)

    parenttitle = ""
    responses = []
    # Step 2: Process each class
    for entity in entities:
        class_name = entity["name"]
        footnotes = extract_footnotes(class_name, dir, foot_note_list)

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
            footnotes = footnotes + extract_footnotes(class_name, "general", foot_note_list)
        with open(f"{sourcefolder}/temp/{class_name}.txt", "w", encoding="utf-8") as file:
            file.write(context)
        
        # Summarize each PDF and compile into a text file
        response = ""
        
        if context.strip():
            isParent: bool = False
            fewshots = ["", ""] if entity.get("fewshots") is None else entity["fewshots"]
            startsuggestion = "" if entity.get("sug") is None else entity["sug"]
            if not entity["parent"] == parenttitle:
                parenttitle = entity["parent"]
                responses.append(f'</ul><p>{parenttitle}</p><ul>')
                isParent = True
            response = activate_api(input=input, class_name=class_name, rag_inf=context, isParent=isParent, footnotes=footnotes)
            responses.append(response)
        print(response)
           
    final_resp = " ".join(responses)
    
    final_resp = final_resp[len("</ul>"):]
    final_resp = f"""<p>{give_conlusion(final_resp, entity["name"], input, 0)}</p><div style="display: block">Further Details:</div>{final_resp}</ul>"""
    return final_resp



## Testsection

# stri = generateAnswer("HUAWEI nova 12i", "frontend")
# print(stri)
