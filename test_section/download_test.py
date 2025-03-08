from shared.gcs_handler import download_file_from_bucket

folder = "test-Section"
file_n = "Fairphone-2023-Impact-Report-.pdf"
download_file_from_bucket("raw_pdf_files",f"raw_pdf_files/fairphone/{file_n}", f"test_section/{file_n}" )