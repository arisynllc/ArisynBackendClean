from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'aac', 'flac'}
MAX_FILE_SIZE = 50 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def health():
    return jsonify({
        "service": "Arisyn AI Vocal Analysis Backend",
        "status": "online",
        "version": "1.0.0",
        "max_file_size": "50MB",
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "endpoints": {"analyze": "/analyze", "health": "/"}
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        # Simulate analysis
        return jsonify({
            "message": "File uploaded and analyzed successfully.",
            "filename": file.filename,
            "analysis_result": "Mock vocal analysis complete."
        })
    else:
        return jsonify({"error": "File type not allowed"}), 400