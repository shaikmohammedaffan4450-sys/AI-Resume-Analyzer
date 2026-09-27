"""Flask application for the AI Resume Analyzer."""

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge

from matcher import analyze_resume
from resume_parser import ResumeParseError, extract_text_from_pdf


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
MAX_RESUME_SIZE = 8 * 1024 * 1024

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
# Leave room for multipart fields and boundaries beyond the PDF's own size cap.
app.config["MAX_CONTENT_LENGTH"] = MAX_RESUME_SIZE + 64 * 1024


@app.get("/")
def index():
    """Serve the single-page frontend from Flask."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/api/analyze")
def analyze():
    """Extract resume text and compare its skills with a job description."""
    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if resume_file is None or not resume_file.filename:
        return jsonify(error="Choose a PDF resume to analyze."), 400
    if not resume_file.filename.lower().endswith(".pdf"):
        return jsonify(error="The resume must be a PDF file."), 400
    if not job_description:
        return jsonify(error="Paste a job description before analyzing."), 400

    # Werkzeug provides a seekable temporary stream for multipart uploads.
    resume_file.stream.seek(0, 2)
    resume_size = resume_file.stream.tell()
    resume_file.stream.seek(0)
    if resume_size > MAX_RESUME_SIZE:
        return jsonify(error="The upload is too large. Choose a PDF no larger than 8 MB."), 413

    try:
        # Parse the request stream directly; resume files are never saved to disk.
        resume_text = extract_text_from_pdf(resume_file.stream)
        result = analyze_resume(resume_text, job_description)
    except ResumeParseError as exc:
        return jsonify(error=str(exc)), 400
    except Exception:
        app.logger.exception("Resume analysis failed")
        return jsonify(error="The resume could not be analyzed. Check the PDF and try again."), 500

    result["resume_text"] = resume_text
    return jsonify(result)


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(_error):
    """Return a friendly JSON response when the request exceeds 8 MB."""
    return jsonify(error="The upload is too large. Choose a PDF smaller than 8 MB."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)