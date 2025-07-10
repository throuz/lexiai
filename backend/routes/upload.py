from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import db, FileRecord
import os
import PyPDF2

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) if file.filename else None
        if not filename:
            return jsonify({"error": "Invalid filename"}), 400
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        # Extract text
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        # 新增資料庫紀錄
        record = FileRecord(filename=filename, text=text)
        db.session.add(record)
        db.session.commit()
        return jsonify({"filename": filename, "text": text, "id": record.id})
    return jsonify({"error": "Invalid file type"}), 400
