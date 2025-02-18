"""
TODO: allow multiple entities
"""
from openai import OpenAI
from shared.ind_key import rand_k
import json
from google.api_core.exceptions import NotFound
from shared.gcs_handler import download_file_from_bucket, create_temp_folder
from shared.git_handler import load_class_data_from_git
from shared.test_center import conclusion_tester
import random
from pydantic import BaseModel
from shared.prefilter_extractor import extract_comp_name
from shared.structured_output_creator import InterpreterFormatWithAdjectiveStructure
from shared.json_processor import create_json_file

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
def give_conlusion(previous_text:str, phone_name, count)->str:
    context = f"""
    You are a knowledgeable and concise assistant providing conclusions about the environmental footprint of smartphones.
    Your task is to analyze and describe the as-is situation and its direct impact on the environmental footprint.
    - Base your response exclusively on the information provided between the <input> brackets: <input> {previous_text} </input>.
    - Avoid suggesting improvements or speculating on ways to reduce the environmental footprint.
    - Keep your answer brief yet informative, aiming for approximately 50 tokens in length.
    - Maintain a professional and objective tone in your response.

    Stay focused on the provided content and deliver clear, concise conclusions.
    """


    question = f"""
    Provide a brief summary of the carbon footprint of the {phone_name}. 
    In your summary, indicate whether the phone likely has a positive (good) or negative (bad) impact on the environmental footprint.
    """

    
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
        """
        text_parts: list[str] = generated_text.split(",")
        print(f"outclist: {text_parts}")
        bold_text: str = f"<span style="font-weight: bold">{text_parts[len(text_parts)-1]}<span>"
        generated_text: str = ",".join(text_parts[:-1])
        generated_text = generated_text + "," + bold_text
        """
        return generated_text
    elif count < 4: 
        count = count + 1
        return give_conlusion(previous_text, phone_name, count)
    else:
        return "An Error happened generating the summary"


def activate_api(input: str, question: str, rag_inf: str, comp)  -> dict:

    comp_add = ""

    if not comp == "general":

        comp_add = f", and summarize {comp}'s improvement efforts"




    # comment = f""" Give the responses in the style of the following examples: Question: {fewshot_question} Answer: {fewshots[0]} Question: {fewshot_question} Answer: {fewshots[1]}"""
    context = f"""
    You are a knowledgeable and concise assistant providing reviews about the environmental footprint of the {input} by {comp}.\n
    Your task is to analyze the provided information regarding the as-is situation, evaluate its environmental impact{comp_add}.\n
    For that you will receive textual documents about various environmet-related aspects. \n
    - Base your response strictly on the content provided between the <input> brackets: <input> {rag_inf} </input>.\n
    - Avoid suggesting improvements or discussing potential changes to the environmental footprint.\n
    - Each category should receive one or two adjectives summarizing the environmental impact. If two adjectives are used, connect them with an appropriate conjunction like "and" or "but."\n


    **Structure:**\n
    Give a structured response, by provoding text for the presented categories and sub-categories. Further each subcategory consists of...
    1. A concise description of the as-is situation and its environmental impact {comp_add}.\n
    2. One or two adjectives summarizing the environmental impact.\n

    Stay focused, objective, and concise in your analysis.\n
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
        temperature=0.5,
        response_format=InterpreterFormatWithAdjectiveStructure
    )

    generated_answer:str = completion.choices[0].message.content
    """
    generated_answer_dict:dict = json.loads(generated_answer)
    
    generated_text:str = generated_answer_dict["summary"]
    generated_adj:str = generated_answer_dict["adjective"]
    generated_adj = generated_adj.capitalize()
    if not isParent:
        generated_text = replace_sentence_start(generated_text, input)

    html_output = ''.join(f'{line} ' for line in generated_text.split('\n') if line.strip())

    resp_dict: dict = {"class_name": class_name, "generated_adj": generated_adj, "html_output": html_output, "footnotes_span": footnotes_span}
    """

    return json.loads(generated_answer)

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

def get_parent_name(data: list, json_code: str)->dict:
    for el in data:
        if el["json_name"] == json_code:
            inner_items = el["list"]
            return {"name": el["name"], "list": inner_items}
    return "Couldn't find name"

def get_entity_name(data: list[dict], json_code: str)->str:
    for el in data:
        if el["json_name"] == json_code:
            return el["name"]
    return "Couldn't find name"


def generateAnswer(input: str, sourcefolder, string_mode=True)->dict:
    bucket_name = "raw_pdf_files"
    
    create_temp_folder(sourcefolder)
    brandlist: list[str] = download_and_extract_json("all_companies", sourcefolder)
    foot_note_list: list[dict] = download_and_extract_json("footnotes", sourcefolder)

    # print(foot_note_list)
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
    scores_list = []
    final_responses = []
    # Step 1: Download and read JSON files
    load_class_data_from_git(sourcefolder)
    data = []
    with open(f"{sourcefolder}/temp/classes.json", "r") as file:
        data = json.load(file)
    context = ""
    comp = extract_comp_name(dir)
    prompt = f"""In the following there is a list of questions. 
    Please describe for each the status quo related to the {input} and what the {comp} is doing to improve the situation.\n
    """
    count = 0
    score_name_list: list[str] = []
    for parentcl_ in data:
        # transform data in llm format
        entities = parentcl_["list"]
        responses = []
        isParent = True
        score_name = parentcl_["json_name"]
        score_name_list.append(score_name)
        # Step 2: Process each class
        for entity in entities:
            class_name = entity["name"]
            footnotes = extract_footnotes(class_name, dir, foot_note_list)
            descr = entity["description"]
            css_name = entity["json_name"]
            context = context + f"\n \n##{class_name}##\n \n"
            try:
                download_file_from_bucket(bucket_name, f"summaries_struct_c/{dir}-{class_name}.txt", f"{sourcefolder}/temp/{dir}-{class_name}.txt")
                context =  context + getContext(dir, class_name, sourcefolder) +"\n"
            except NotFound:
                print(f"file summaries_struct_c/{dir}-{class_name}.txt not found")



                footnotes = footnotes + extract_footnotes(class_name, "general", foot_note_list)
            #   with open(f"{sourcefolder}/temp/{class_name}.txt", "w", encoding="utf-8") as file:
            #     file.write(context)
            class_description: str = descr
            class_description = class_description.replace("<replacer>", input)
            

            prompt = prompt + class_description + "\n"
            count = count + 1
            
    prompt = prompt + f"Your answer should in total consist at least of {str(count * 50  + 100)} tokens."
    if not dir == "general":
        try:
            download_file_from_bucket(bucket_name, f"summaries_struct_c/general-{class_name}.txt", f"{sourcefolder}/temp/general-{class_name}.txt")
            context = get_element_by_name(f"{sourcefolder}/temp/scraped-{dir}-data.json", input) + context + getContext("general", class_name, sourcefolder) 
        except NotFound:
            print(f"file summaries_struct_c/general-{class_name}.txt not found")
    if context.strip():

        response_dic: dict = activate_api(input=input, question=prompt, rag_inf=context, comp=comp)
        



    final_resp = ""
    for sc_ in score_name_list:
        enity_dic: dict = response_dic[sc_]
        summary_col: str = ""
        sc_dict = get_parent_name(data=data, json_code=sc_)
        for value in enity_dic.values(): 
            summary: str = value["summary"]
            summary_col = f"{summary_col} {summary}"
            value["class_name"] = get_entity_name(data=sc_dict["list"], json_code=value)
        response_dic[sc_]["name"] = sc_dict["name"]
           
        final_resp = final_resp + f" {summary_col}"

    conclusion = give_conlusion(final_resp, input, 0)
    response_dic["conclusion"] = {"summary": conclusion}
    response_dic["name"] = input

    save_file = f"{sourcefolder}/temp/generated_reviews_no_score.json"
    create_json_file(response_dic, "", save_file)

    return response_dic



    """
    final_responses.append(generate_html_output(resp=responses, parent=parentcl_, score_dict=score))
        
    scores_list.append(score["score"]) 

    totalscore = get_total_score(scores_list)
    
    final_html_resp = generate_final_answer(conclusion, final_resp, totalscore)
    if string_mode:
        return final_html_resp
    else:
        return {"answer": final_html_resp, "score": totalscore}
    """



## Testsection
#print(generateAnswer("iPhone 16","frontend"))
#print(generateAnswer("Fairphone 5","text_generator"))
