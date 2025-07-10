from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS
from models import db
from routes.upload import upload_bp
from routes.summarize import summarize_bp
from routes.qa import qa_bp
import openai

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# SQLAlchemy 設定
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

CORS(
    app,
    origins=[
        "http://localhost:3000",
        "https://lexiai-pi.vercel.app",
        "https://lexiai-throuzs-projects.vercel.app",
        "https://lexiai-git-main-throuzs-projects.vercel.app",
    ],
)

# 註冊 blueprint
app.register_blueprint(upload_bp)
app.register_blueprint(summarize_bp)
app.register_blueprint(qa_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
