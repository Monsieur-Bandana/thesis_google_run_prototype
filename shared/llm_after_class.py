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
from shared.structured_output_creator import (
    InterpreterFormatWithAdjectiveStructure,
    create_inner_struct,
)
from shared.json_processor import create_json_file
from shared.question_builder import (
    generate_context_for_llm,
    create_final_prompt,
)
import tiktoken

sk = rand_k
client = OpenAI(api_key=sk)
data = []
min_token_size = 40


def get_token_length(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def replace_sentence_start(sentence: str, input):
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
        "Extending this idea, the phone",
    ]

    # Check if the sentence starts with "The HUAWEI Pura 70 Ultra"
    if sentence.startswith(f"The {input}"):
        # Replace the starting phrase with a randomly chosen phrase from the list
        return random.choice(starting_phrases) + sentence[len(f"The {input}") :]

    # Return the original sentence if no match
    return sentence


# from ind_key import key
def give_conlusion(previous_text: str, phone_name, count) -> str:
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
    Provide a brief summary of the environmental footprint of the {phone_name}. 
    In your summary, indicate whether the phone likely has a high (which is bad) or relatively low (which is better) impact on the environmental footprint.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question},
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


def activate_api(
    input: str, question: str, rag_inf: str, comp, json_strct: dict
) -> dict:

    comp_add = ""

    if not comp == "general":

        comp_add = f", and summarize {comp}'s improvement efforts"

    # comment = f""" Give the responses in the style of the following examples: Question: {fewshot_question} Answer: {fewshots[0]} Question: {fewshot_question} Answer: {fewshots[1]}"""
    context = generate_context_for_llm(
        phone_n=input, comp_add=comp_add, comp=comp, rag_inf=rag_inf
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question},
        ],
        functions=[
            {
                "name": "structured_response",
                "description": "Generate a structured response following a strict JSON schema.",
                "parameters": json_strct,
            }
        ],
        function_call={"name": "structured_response"},
        temperature=0.5,
    )

    # TODO: function json statt baseclass
    # für jedes class element fügen wir per code noch die paramter hinzu ...[paramters] sowie die standardfrage [interpreter wird zu descripotion gepackt] tokens removed
    js_resp = completion.choices[0].message.function_call.arguments
    structured_response = json.loads(
        completion.choices[0].message.function_call.arguments
    )
    print(js_resp)

    return structured_response


def getContext(dir, class_name, sourcefolder):
    local_file_path = f"{sourcefolder}/temp/{dir}-{class_name}.txt"
    try:
        with open(local_file_path, "r", encoding="utf-8") as file:
            print(f"extracted text from {local_file_path}")
            context = file.read()
    except UnicodeDecodeError:
        with open(local_file_path, "r", encoding="ISO-8859-1") as file:
            context = file.read()
    return context


def get_element_by_name(file_path, input_name):
    try:
        # Open and load the JSON file
        with open(file_path, "r") as file:
            data: list[dict] = json.load(file)

        # Iterate over the list of entities in the JSON
        for entity in data:
            if entity.get("name") == input_name:
                return entity.get("specs", "specs not found for this entity")

        return f"No entity found with the name '{input_name}'."
    except FileNotFoundError:
        return f"The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return "Error decoding JSON. Please check the file format."


def download_and_extract_json(file_name, sourcefolder) -> list:
    download_file_from_bucket(
        "raw_pdf_files",
        f"json_files/{file_name}.json",
        f"{sourcefolder}/temp/{file_name}.json",
    )
    outc_list = []
    with open(f"{sourcefolder}/temp/{file_name}.json", "r") as file:
        outc_list = json.load(file)
    return outc_list


def extract_footnotes(class_n, dir_, foot_note_list: list[dict]) -> list:
    outc_list: list[int] = []
    for el in foot_note_list:
        if el["name"] == class_n:
            footnotes: list[dict] = el["footnotes"]
            for fel in footnotes:
                if fel["category"] == dir_:
                    outc_list.append(fel["footnote"])
    return outc_list


def get_parent_name(data: list, json_code: str) -> dict:
    for el in data:
        if el["json_name"] == json_code:
            inner_items = el["list"]
            return {"name": el["name"], "list": inner_items}
    return "Couldn't find name"


def get_entity_name(parent: str, json_code: str) -> str:
    for el in data:
        if el["json_name"] == parent:
            for el2 in el["list"]:
                if el2["json_name"] == json_code:
                    return el2["name"]
    return "Couldn't find name"


def correctAdjectives(dicti: dict, nested=False) -> dict:
    """
    from leading adjectives removes unwanted character '.', further capitalizes adjectives
    """
    if nested:
        for key, val in dicti.items():
            for key2, val2 in val.items():
                adj: str = val2["adjective"]
                adj = adj.replace(".", "")
                adj = adj.capitalize()
                val2["adjective"] = adj
        return dicti
    for key, val in dicti.items():
        adj: str = val["adjective"]
        adj = adj.replace(".", "")
        adj = adj.capitalize()
        val["adjective"] = adj
    return dicti


def create_empty_new_dict():
    new_dict: dict = {}
    for ent in data:
        k = ent["json_name"]
        new_dict[k] = {"name": ent["name"]}
        for el in ent["list"]:
            k2 = el["json_name"]
            new_dict[k][k2] = {"class_name": el["name"]}
    return new_dict


def generateAnswer(input: str, sourcefolder) -> dict:
    bucket_name = "raw_pdf_files"

    create_temp_folder(sourcefolder)
    brandlist: list[str] = download_and_extract_json("all_companies", sourcefolder)

    # print(foot_note_list)
    brandlist.append("general")

    # set generall as standard brand
    dir = "general"
    # overwrite standard brand by actual brand
    for brand in brandlist:
        if brand in input.lower():
            print(f"{brand} found in request {input.lower()}")
            dir = brand
            download_file_from_bucket(
                bucket_name,
                f"json_files/scraped-{dir}-data.json",
                f"{sourcefolder}/temp/scraped-{dir}-data.json",
            )
        else:
            print(f"{brand} not found in request {input}")

    load_class_data_from_git(sourcefolder)
    global data
    with open(f"{sourcefolder}/temp/classes.json", "r") as file:
        data = json.load(file)
    context = ""
    comp = extract_comp_name(dir)

    count = 0
    score_name_list: list[str] = []
    json_strct = {"type": "object", "properties": {}}
    required_sub_list = []
    for parentcl_ in data:
        # transform data in llm format
        entities = parentcl_["list"]
        score_name = parentcl_["json_name"]
        score_name_list.append(score_name)
        # Step 2: Process each class
        for entity in entities:
            class_name = entity["name"]
            descr = entity["description"]
            css_name = entity["json_name"]
            context = context + f"\n \n##{class_name}##\n \n"
            download_file_from_bucket(
                bucket_name,
                f"summaries/{dir}-{css_name}3.txt",
                f"{sourcefolder}/temp/{dir}-{css_name}.txt",
            )
            try:
                context += getContext(dir, css_name, sourcefolder) + "\n"
            except NotFound:
                print(f"file summaries_struct_c/{dir}-{css_name}.txt not found")

            if dir != "general":
                download_file_from_bucket(
                    bucket_name,
                    f"summaries/general-{css_name}3.txt",
                    f"{sourcefolder}/temp/general-{css_name}.txt",
                )
                try:
                    context += getContext("general", css_name, sourcefolder)
                except NotFound:
                    print(f"file summaries/general-{css_name}.txt not found")

            #  footnotes = footnotes + extract_footnotes(class_name, "general", foot_note_list)
            #   with open(f"{sourcefolder}/temp/{class_name}.txt", "w", encoding="utf-8") as file:
            #     file.write(context)
            class_description: str = descr
            class_description = class_description.replace("<replacer>", input)
            prompt = ""
            prompt += f"""How would you assess the {class_name} of the {input} by {comp}? 
            Does it have a high or low impact on the {input}'s environmental footprint? 
            What factors contribute to your evaluation? \n"""
            prompt += class_description + "\n"
            # prompt += create_final_prompt(topic=class_name, input=input)
            prompt = prompt.replace('"', "")
            prompt = prompt.replace("'", "")
            required_sub_list.append(css_name)
            json_strct["properties"][css_name] = create_inner_struct(
                descr=prompt, min_token_size=min_token_size
            )
            count += 1

    json_strct["required"] = required_sub_list

    prompt = f"""
    You will receive the description of a the phone {input}.
    Conduct a environmental-focused analysis on this phone, based on it's data, your context data and given structure.
    """

    prompt += "Phone information:"
    prompt += get_element_by_name(f"{sourcefolder}/temp/scraped-{dir}-data.json", input)
    ## hier einbauen: while loop
    trial_counter = 0
    resp_options = []
    size_val = count * min_token_size
    print(json_strct)
    # input("Enter")
    best_val = 0
    while trial_counter < 5:

        # try:
        response_dic: dict = activate_api(
            input=input,
            question=prompt,
            rag_inf=context,
            comp=comp,
            json_strct=json_strct,
        )
        final_resp = ""
        for key, val in response_dic.items():
            final_resp += f"""{ val["summary"]}"""
        """
        lengthL.append(get_token_length(str(token_mes_str)))
        with open(
            f"test_section/dsasd-outcome.json", "w", encoding="utf-8"
        ) as file:
            json.dump(lengthL, file, indent=4)
        """

        print(response_dic)
        # input("Press Enter to continue...")
        response_dic = correctAdjectives(response_dic)

        # print(response_dic)

        final_dic_for_further_processing: dict = create_empty_new_dict()
        for key1, val1 in final_dic_for_further_processing.items():
            sub_dict: dict = val1
            for key2 in sub_dict.keys():
                if key2 in response_dic:
                    for str_k in ["adjective", "summary"]:
                        final_dic_for_further_processing[key1][key2][str_k] = (
                            response_dic[key2][str_k]
                        )

        # expected:40 per token -> ideally 440 tokens or 540
        text_len = get_token_length(final_resp)
        if (size_val - 0) <= text_len <= (size_val + 100):
            resp_options = []
            best_val = text_len
            break
        print(f"size at {text_len} ->repeat")
        resp_options.append({"len": text_len, "cont": final_dic_for_further_processing})
        trial_counter += 1
        # except:
        #   print("problem at interprete")
        #   trial_counter -= 1
    # in case no answer fits into conditions
    other_options = ""
    for opt in resp_options:
        other_options += f"""{opt["len"]}, """

    def closest_to_range(values, lower=(size_val - 0), upper=(size_val + 100)):
        closest_value = min(values, key=lambda x: min(abs(x - lower), abs(x - upper)))
        return closest_value

    if resp_options:
        val_list = []
        for r in resp_options:
            val_list.append(r["len"])
        best_val = closest_to_range(values=val_list)
        for r in resp_options:
            if best_val == r["len"]:
                final_dic_for_further_processing = r["cont"]

    with open(
        f"{sourcefolder}/temp/{input}-context.txt", "w", encoding="utf-8"
    ) as file:
        file.write(f"{prompt}\n{context}")
    with open(
        f"{sourcefolder}/temp/length_collector.txt", "a", encoding="utf-8"
    ) as file:
        file.write(f"{input}:   {best_val} other options: {other_options}\n")
    conclusion = give_conlusion(final_resp, input, 0)
    final_dic_for_further_processing["conclusion"] = {"summary": conclusion}
    final_dic_for_further_processing["name"] = input

    lit_file = f"{sourcefolder}/temp/literature"
    download_file_from_bucket(
        "raw_pdf_files",
        f"json_files/literature.json",
        lit_file,
    )

    with open(lit_file, "r") as file:
        literature_links = json.load(file)
    library = []
    if dir != "general":
        library += literature_links[dir]
    library += literature_links["general"]
    final_dic_for_further_processing["sources"] = library

    save_file = f"{sourcefolder}/temp/generated_reviews_no_score.json"
    create_json_file(final_dic_for_further_processing, "", save_file)

    return final_dic_for_further_processing

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
# print(generateAnswer("iPhone 16","frontend"))
# print(generateAnswer("Fairphone 5","text_generator"))
