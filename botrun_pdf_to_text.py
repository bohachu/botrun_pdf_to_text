import os
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader
from typing import List, Optional


def convert_pdf_to_txt(file_path: str) -> None:
    # Check if already converted
    if os.path.exists(file_path.replace(".pdf", ".txt")):
        print(f"Skipped (already converted): {file_path}")
        return

    try:
        print(f"Converting: {file_path}")
        reader = PdfReader(file_path)
        texts = [page.extract_text() for page in reader.pages]
        text = ''.join(texts)
        with open(file_path.replace(".pdf", ".txt"), "w") as text_file:
            text_file.write(text)
        print(f"Converted: {file_path}")
    except Exception as e:
        print(f"Error converting {file_path}. Reason: {e}")


def botrun_pdf_to_text_folder(folder_path: str) -> None:
    files_to_convert = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                files_to_convert.append(os.path.join(root, file))

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        executor.map(convert_pdf_to_txt, files_to_convert)


def botrun_pdf_to_text_files(file_list: List[str]) -> None:
    files_to_convert = [file_path for file_path in file_list if file_path.endswith(".pdf")]

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        executor.map(convert_pdf_to_txt, files_to_convert)


if __name__ == "__main__":
    botrun_pdf_to_text_folder("./users/cbh_cameo_tw/data/upload_files")
    botrun_pdf_to_text_files(["./users/cbh_cameo_tw/data/upload_files/222715345.pdf"])
