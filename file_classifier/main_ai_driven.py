"""
classifies the source-files

"""

from PyPDF2 import PdfReader
from llama_index.core import SimpleDirectoryReader
import json
import os
from classif_str import InterpreterFormatOnDominance, RelatabilityByFloat
from shared.json_processor import create_json_file
from shared.git_handler import load_class_data_from_git
from pdf_handler import create_pdf_temp_folder
from shared.gcs_handler import (
    upload_file,
    download_file_from_bucket,
    list_directories_in_bucket,
    create_temp_folder,
)
from sources_handler import add_footnotes
from openai import OpenAI
from shared.ind_key import rand_k
import re
from shared.question_builder import (
    generate_comp_related_question,
    create_general_question,
    generate_context_for_classifier,
)

# saves the details about the EF-categories
classes = []
bucket_name = "raw_pdf_files"
folder_name = "file_classifier"
# collects the files, which already got classified
already_classified = []


def extract_classes() -> list:
    load_class_data_from_git(folder_name)
    with open(f"{folder_name}/temp/classes.json", "r") as file:
        data: list = json.load(file)
    return data


def classify_text_using_retriever(dir: str, classes) -> list[dict]:

    pdf_docs = create_pdf_temp_folder(bucket_name, folder_name, dir)
    chunk_size = 100000

    pdf_list = [file for file in os.listdir(pdf_docs) if file.lower().endswith(".pdf")]
    print(pdf_list)

    reader = SimpleDirectoryReader(
        input_dir=pdf_docs,
        recursive=True,
    )
    collection: list[dict] = []
    pdf_list = [item for item in pdf_list if item not in already_classified]

    for pdf_file_path in pdf_list:
        reader = PdfReader(f"{folder_name}/temp/{dir}/{pdf_file_path}")
        content = ""
        for page in reader.pages:
            page_text = page.extract_text()
            lines = page_text.split("\n")

            # remove references section, to prevent classifier confusing literature with textual content
            for line in lines:
                if line.strip().lower() == "references":
                    break
                content += line + "\n"
            else:
                continue
            break

        with open(
            f"{folder_name}/temp/contents--{pdf_file_path[0:8]}.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(content)

        content_chunks = [
            content[i : i + chunk_size] for i in range(0, len(content), chunk_size)
        ]

        # count chunks to enable the classifier to store file name and chunk number into the final file
        chunk_nr = 0
        answeres_list = []
        # loops thorugh chunks, for each chunk it does a new API call for each EF-category.
        for content in content_chunks:
            for cl in classes:
                for subcl in cl["list"]:
                    question = ""
                    descr: str = subcl["description"]
                    name = subcl["name"]
                    question = create_general_question(name)
                    question += descr
                    try:
                        question += f"""{subcl["interpreter"]}"""
                    except:
                        print("no additial quesion")
                    # if file not from general directory, it adds additional questions referring to the company to the prompt
                    if not dir == "general":
                        question += generate_comp_related_question(name, dir)
                        question = question.replace("<replacer>", dir)
                    else:
                        question = question.replace("<replacer>", "smart")

                    sk = rand_k
                    client = OpenAI(api_key=sk)

                    context = generate_context_for_classifier(content=content)

                    response = client.beta.chat.completions.parse(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": context},
                            {"role": "user", "content": question},
                        ],
                        temperature=0.2,
                        # response_format instructs the LLM to return a numeric value
                        response_format=RelatabilityByFloat,
                    )
                    summary = response.choices[0].message.content
                    generated_answer_dict: dict = json.loads(summary)
                    json_name = subcl["json_name"]
                    answeres_list.append({json_name: generated_answer_dict})

            final_anser_dict = {
                "source": f"{pdf_file_path}-chunk-{chunk_nr}",
                "answeres": answeres_list,
                "brand": dir,
            }

            create_json_file(
                final_anser_dict,
                "file_classifier",
                f"{folder_name}/temp/save_file.json",
            )
            chunk_nr = chunk_nr + 1

    return collection


if __name__ == "__main__":
    # for each directory in google cloud storage:
    prefix = "raw_pdf_files/"
    # the files are stored in seperate directories, depending from the brand
    directories = list_directories_in_bucket(bucket_name, prefix)
    print(directories)

    create_temp_folder(folder_name)
    if not classes:
        classes = extract_classes()
    # checks which files already got classified
    try:
        download_file_from_bucket(
            "raw_pdf_files",
            "json_files/docs_with_labels.json",
            f"{folder_name}/temp/save_file2.json",
        )
        with open(f"{folder_name}/temp/save_file2.json", "r") as file:
            data2 = json.load(file)
        for el in data2:
            el_name: str = el["source"]
            el_name = el_name.split("-chunk-")[0]
            already_classified.append(el_name)
    except:
        print("file 'save_file2.json' does not exist")

    for directory in directories:

        text_classifications: list[dict] = classify_text_using_retriever(
            directory, classes
        )

    # if all files are already classified there is no save_file
    try:
        with open(f"{folder_name}/temp/save_file.json", "r") as file:
            data = json.load(file)
        outc_l: list[dict] = []

        for el in data:
            class_list = []

            som_l: dict = el["answeres"]

            for el_dict in som_l:
                for key, el2 in el_dict.items():
                    print(el2)
                    print(key)
                    if el2["probability"] >= 0.5:
                        cl_name = key
                        if key not in class_list:
                            class_list.append(key)
            output_file = f"{folder_name}/temp/save_file2.json"
            outc_l.append(
                {"source": el["source"], "list": class_list, "brand": el["brand"]}
            )
        with open(output_file, "w") as file:
            json.dump(outc_l, file, indent=4)
            # bucket_name, source_file_name, destination_blob_name, folder_name=None
        upload_file(bucket_name, output_file, "json_files/docs_with_labels.json")
    except:
        print("no file got interpreted")
