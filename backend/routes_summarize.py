from flask import Blueprint, request, jsonify
from models import db, FileRecord
import openai

summarize_bp = Blueprint("summarize", __name__)


@summarize_bp.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text")
    record_id = data.get("id")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    prompt = f"請將以下法律文件內容摘要成重點，並以完整句子結尾，且每一點都要有詳細說明，總字數不少於 500 字：\n{text}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        content = response.choices[0].message.content
        summary = content.strip() if content else ""
        # 更新資料庫紀錄
        if record_id:
            record = FileRecord.query.get(record_id)
            if record:
                record.summary = summary
                db.session.commit()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
