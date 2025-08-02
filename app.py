# app.py
from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
from rag import get_context
import json
from openai import OpenAI

# Load API key từ .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Khởi tạo OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Lấy context từ tài liệu (RAG)
    context = get_context(user_message)

    # Gọi OpenAI API (GPT-3.5-Turbo)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là một nhân viên tư vấn du lịch chuyên nghiệp, trả lời ngắn gọn, dễ hiểu."},
            {"role": "user", "content": f"{context}\n\nCâu hỏi của khách: {user_message}"}
        ]
    )
    assistant_message = response.choices[0].message.content

    # Lưu vào logs.json
    log_entry = {"user": user_message, "assistant": assistant_message}
    if os.path.exists("logs.json"):
        with open("logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open("logs.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    return jsonify({"response": assistant_message})

if __name__ == "__main__":
    app.run(debug=True)from flask import Flask, request, render_template_string
import os
from langchain.document_loaders import TextLoader

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.txt'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            loader = TextLoader(filepath)
            docs = loader.load()
            print("📝 Dữ liệu vừa upload:")
            for i, doc in enumerate(docs):
                print(f"[Trang {i+1}] {doc.page_content[:500]}...")

            return "✅ Upload thành công và dữ liệu đã được xử lý."
        else:
            return "❌ Chỉ chấp nhận file .txt"

    # Form upload đơn giản
    return render_template_string('''
        <h2>Upload file .txt</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".txt">
            <input type="submit" value="Upload">
        </form>
    ''')
