import os
import threading
from queue import Queue
from pypdf import PdfReader


def convert_pdf_to_txt(file_path):
    # 檢查是否已經轉換過
    if os.path.exists(file_path.replace(".pdf", ".txt")):
        print(f"Skipped (already converted): {file_path}")
        return

    print(f"Converting: {file_path}")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    with open(file_path.replace(".pdf", ".txt"), "w") as text_file:
        text_file.write(text)
    print(f"Converted: {file_path}")


def worker():
    while True:
        file_path = q.get()
        if file_path is None:
            break
        convert_pdf_to_txt(file_path)
        q.task_done()


def botrun_pdf_to_text(input_data):
    global q
    q = Queue()
    threads = []

    # 判斷 input_data 是 folder 還是檔案路徑列表
    if isinstance(input_data, str):
        for root, _, files in os.walk(input_data):
            for file in files:
                if file.endswith(".pdf"):
                    q.put(os.path.join(root, file))
    elif isinstance(input_data, list):
        for file_path in input_data:
            if file_path.endswith(".pdf"):
                q.put(file_path)

    # 啟動 10 個 threads
    for i in range(10):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    q.join()

    # 停止 workers
    for i in range(10):
        q.put(None)
    for t in threads:
        t.join()

# 使用方法：
# 轉換指定 folder 底下的所有 PDFs:
# botrun_pdf_to_text("/path/to/folder")

# 轉換指定的 PDF 檔案路徑列表:
# botrun_pdf_to_text(["/path/to/file1.pdf", "/path/to/file2.pdf"])
