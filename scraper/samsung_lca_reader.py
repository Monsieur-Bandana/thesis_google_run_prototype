from shared.gcs_handler import download_file_from_bucket, upload_file
import json
from PyPDF2 import PdfReader
import pdfplumber

with open("scraper/temp/scraped-galaxy-data.json", "r") as file:
    data: list[dict] = json.load(file)

pdf_file_path = "scraper/temp/lca.pdf"

download_file_from_bucket(
    "raw_pdf_files",
    "raw_pdf_files/galaxy/LCA_Results_for_Smartphones.pdf",
    pdf_file_path,
)

import fitz
import io
from PIL import Image


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


extract_images_from_pdf(pdf_file_path)
