from flask import Blueprint, request, jsonify
import openai

qa_bp = Blueprint("qa", __name__)


@qa_bp.route("/qa", methods=["POST"])
def qa():
    data = request.get_json()
    text = data.get("text")
    question = data.get("question")
    if not text or not question:
        return jsonify({"error": "Text and question required"}), 400
    prompt = f"根據以下法律文件內容詳細回答問題，請以完整句子結尾，並展開說明每一點，總字數不少於 500 字：\n{text}\n\n問題：{question}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        content = response.choices[0].message.content
        answer = content.strip() if content else ""
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
