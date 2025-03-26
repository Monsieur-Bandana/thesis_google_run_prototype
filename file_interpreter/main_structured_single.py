import json
import os
from PyPDF2 import PdfReader
from openai import OpenAI

# from ind_key import rand_k
from txt_generator import process_json_to_text
from json_processor import (
    merge_json_information,
    create_json_file,
    check_file_got_already_interpreted,
)
from shared.git_handler import load_class_data_from_git
from shared.gcs_handler import (
    list_files_in_folder,
    download_file_from_bucket,
    upload_file,
    list_directories_in_bucket,
    create_temp_folder,
)
from shared.ind_key import rand_k
from class_contructor import InterpreterStructure
from shared.question_builder import (
    create_general_question,
    generate_comp_related_question,
)

# Configure your Google Cloud and OpenAI API credentials
sk = rand_k
main_folder = "file_interpreter"
prefix = "raw_pdf_files/"
bucket_name = "raw_pdf_files"
labels_data = []
interpreted_files = []
upload_data = []


def execute_summary(prompt, chunk, comp, chunk_nr, pdf_file_path):

    client = OpenAI(api_key=sk)
    context_1 = f"""
                You are a helpful assistant tasked with extracting information about Smartphones and their environmental impact. \n

                """

    if not comp == "general":
        context_1 = f"""
                    You are a helpful assistant tasked with extracting information about {comp}-Smartphones, also referred to as {dir}-Smartphones and their environmental impact. \n
                    - Focus exclusively on information that directly pertains to {comp} and its products, such as the {comp}-Smartphone, as mentioned in the provided text. \n
                    - Ensure the name "{comp}" is explicitly mentioned in your response where relevant. \n
                    - Ignore general information about the smartphone industry unless it explicitly relates to {comp}. \n

                    """

    context_2 = f"""
                Your responsibilities are as follows:\n
                - Summarize key points in concise bullet points.\n
                - Extract specific details, including important figures, data, and statistics, where available, while keeping the response concise.\n

                **Important Instructions**:\n
                - Use only the information provided in the following text as your source. Do not incorporate any external knowledge or assumptions.\n
                - You will receive a large set of questions. You don't need to answer every question. Answer only the questions where you find answers in the text to.\n
                - If no relevant information is found in the provided text, return following string (`"..."`) instead of attempting to answer the question.\n
                - Format your response according to the given structure.\n

                - for each topic we have the following questions:\n

                \n<text>{chunk}</text>\n

                """
    context = context_1 + context_2

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Oder ein anderes Modell wie "gpt-4"
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ],
        )

        summary = response.choices[0].message.content
        return summary

    except:

        print(f"Chunk {chunk_nr} of {pdf_file_path} could not be interpreted")


def checkForInterpreteFiles():
    file_n = "already_interpreted_files.json"
    download_file_from_bucket(
        "raw_pdf_files", f"json_files/{file_n}", f"{main_folder}/temp/{file_n}"
    )
    try:
        with open(f"{main_folder}/temp/{file_n}", "r") as file:
            global interpreted_files
            interpreted_files = json.load(file)
    except:
        print("no interpreted entries yet!")


def main():

    # download classifier index
    pdf_class_file = f"{main_folder}/temp/docs_with_labels.json"
    download_file_from_bucket(
        "raw_pdf_files", "json_files/docs_with_labels.json", pdf_class_file
    )
    global labels_data
    with open(pdf_class_file, "r") as file:
        labels_data = json.load(file)

    # create list of subclasses
    subclasses = []
    load_class_data_from_git(main_folder)
    with open(f"{main_folder}/temp/classes.json", "r") as file:
        entities = json.load(file)
    for ent in entities:
        subclasses += ent["list"]

    # generate company names
    brandlist = list_directories_in_bucket(bucket_name, prefix)
    comps = []
    with open(f"{main_folder}/prefilter.json", "r") as file:
        comps = json.load(file)

    global interpreted_files

    for el in labels_data:
        source_n: str = el["source"]
        file_inf = source_n.split("-chunk-")
        file_n = file_inf[0]
        start_chunk = int(file_inf[1])
        brand = el["brand"]
        dir = "general"
        for cy in comps:
            if cy["product"] == brand:
                dir = cy["company"]
        if source_n not in interpreted_files:
            pdf_file_path = f"{main_folder}/temp/{file_n}"
            download_file_from_bucket(
                bucket_name, f"raw_pdf_files/{brand}/{file_n}", pdf_file_path
            )

            reader = PdfReader(pdf_file_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text()

            chunk_size = 100000  # Adjust chunk size to stay within token limits
            content_chunks = [
                content[i : i + chunk_size] for i in range(0, len(content), chunk_size)
            ]
            chunk = content_chunks[start_chunk]
            for s_class in subclasses:
                class_name = s_class["name"]
                json_name = s_class["json_name"]
                if json_name in el["list"]:
                    question = f"""Topic: {class_name} \n 
                    {create_general_question(class_name)}
                    Further: {s_class["description"]} """
                    try:
                        question += f""" {s_class["interpreter"]}"""
                    except:
                        print("no interpreter questions")
                    if not dir == "general":
                        question += generate_comp_related_question(class_name, dir)

                    summary = execute_summary(
                        prompt=question,
                        chunk=chunk,
                        chunk_nr=start_chunk,
                        pdf_file_path=pdf_file_path,
                        comp=dir,
                    )
                    summary = f"{source_n}\n{summary}\n\n"
                    # check if summary already exists
                    file_n = f"{brand}-{json_name}3.txt"
                    save_file = f"{main_folder}/temp/{file_n}"
                    download_file_from_bucket(
                        destination_file_name=save_file,
                        source_blob_name=f"summaries/{file_n}",
                        bucket_name="raw_pdf_files",
                    )
                    with open(save_file, "a", encoding="utf-8") as file:
                        file.write(summary)
                    global upload_data
                    upload_data.append(save_file)

            interpreted_files.append(source_n)


# for testing upload process
def generateUp():
    brandlist = list_directories_in_bucket(bucket_name, prefix)
    global upload_data
    subclasses = []
    load_class_data_from_git(main_folder)
    with open(f"{main_folder}/temp/classes.json", "r") as file:
        entities = json.load(file)
    for ent in entities:
        subclasses += ent["list"]
    for el in brandlist:
        for el2 in subclasses:
            upload_data.append(f"""{main_folder}/temp/{el}-{el2["json_name"]}3.txt""")
    return upload_data


if __name__ == "__main__":
    create_temp_folder(main_folder)
    checkForInterpreteFiles()
    main()
    file_n = "already_interpreted_files.json"
    with open(f"{main_folder}/temp/{file_n}", "w") as file:
        json.dump(interpreted_files, file, indent=4)
    upload_file("raw_pdf_files", f"{main_folder}/temp/{file_n}", f"json_files/{file_n}")
    for el in upload_data:
        el_phile_name = el.split("/")[2]
        try:
            upload_file("raw_pdf_files", f"{el}", f"summaries/{el_phile_name}")
        except:
            print("leck mi doch am oarschl!!")
