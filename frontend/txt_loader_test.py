from shared.gcs_handler import download_file_from_bucket

bucket = "raw_pdf_files"
file_content = ""
name = "HUAWEI Pura 70"
download_file_from_bucket(bucket, f"pre_rendered_texts/{name}.txt", f"temp/{name}.txt")

with open(f"temp/{name}.txt", 'r') as file:
    # Read the file content
    file_content = file.read()

print(file_content)