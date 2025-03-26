from shared.gcs_handler import download_file_from_bucket, upload_file
import json
from PyPDF2 import PdfReader
import pdfplumber

with open("scraper/temp/scraped-galaxy-data.json", "r") as file:
    data: list[dict] = json.load(file)

pdf_file_path = "scraper/temp/lcagreee.pdf"

download_file_from_bucket(
    "raw_pdf_files",
    "raw_pdf_files/general/greenpeace_ranking.pdf",
    pdf_file_path,
)

import fitz
import io
from PIL import Image


def save_text(text, mode):
    with open(f"scraper/temp/extracted_text{mode}.txt", "w", encoding="utf-8") as file:
        file.write(text)


def createSimplText():
    reader = PdfReader(pdf_file_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    save_text(str(content), "normal")


def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    x = 0
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
            image.save(f"scraper/temp/i{x}.png", format="PNG")

            x += 1
    return images


def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_tables()
            if table:
                tables += table
    save_text(str(tables), "tablemode")
    return tables


createSimplText()
extract_tables_from_pdf(pdf_file_path)
# extract_images_from_pdf(pdf_file_path)
