# rag.py

import os

def get_context(question):
    context = ""
    txt_dir = "./txt_files"

    if not os.path.exists(txt_dir):
        return "Không tìm thấy thư mục txt_files."

    for filename in os.listdir(txt_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(txt_dir, filename), "r", encoding="utf-8") as f:
                context += f.read() + "\n"

    return context[:2000]  # Cắt ngắn nếu cần
