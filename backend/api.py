from flask import Flask, request, jsonify
import os
import PyPDF2
import openai
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 需要安裝：pip install PyPDF2 openai python-dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

openai.api_key = os.getenv('OPENAI_API_KEY')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) if file.filename else None
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Extract text
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join(page.extract_text() or '' for page in reader.pages)
        return jsonify({'filename': filename, 'text': text})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    prompt = f"請將以下法律文件內容摘要成重點：\n{text}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        summary = content.strip() if content else ''
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/qa', methods=['POST'])
def qa():
    data = request.get_json()
    text = data.get('text')
    question = data.get('question')
    if not text or not question:
        return jsonify({'error': 'Text and question required'}), 400
    prompt = f"根據以下法律文件內容回答問題：\n{text}\n\n問題：{question}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        answer = content.strip() if content else ''
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # 啟動方式：python backend/api.py
    app.run(host="0.0.0.0", port=5000, debug=True) 