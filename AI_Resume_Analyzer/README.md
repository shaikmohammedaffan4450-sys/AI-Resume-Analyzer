# AI Resume Analyzer

A small web application that extracts text from a PDF resume and compares its recognized skills with a pasted job description. The project uses local, rule-based matching; it does not call an external AI service and is not a full applicant tracking system (ATS).

## 1. Project Overview

The app helps a student or job seeker spot which skills from a job description are already visible in their resume and which recognized skills may need more attention.

## 2. Problem Statement

Tailoring a resume to a role can be difficult when requirements are dense. This project makes a basic skill comparison visible and understandable, without claiming to predict hiring outcomes.

## 3. Features

- Extract selectable text from PDF resumes.
- Detect skills from a built-in, editable skill catalog.
- Show matching skills, missing skills, resume skills, and job-description skills.
- Calculate a transparent basic skill-match percentage.
- Offer simple, non-prescriptive improvement suggestions.
- Process resumes in memory without storing uploaded files on disk.
- Validate the PDF, required inputs, and an 8 MB upload limit.
- Responsive interface built with HTML, CSS, and vanilla JavaScript.

## 4. Technologies Used

- Python 3.10+
- Flask for the web server and JSON API
- pypdf for PDF text extraction
- HTML, CSS, and vanilla JavaScript for the frontend

## 5. Project Structure

```text
AI_Resume_Analyzer/
├── backend/
│   ├── app.py
│   ├── matcher.py
│   ├── resume_parser.py
│   ├── requirements.txt
│   └── uploads/
│       └── .gitkeep
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
└── README.md
```

## 6. Installation Instructions

Open a terminal in the `AI_Resume_Analyzer` folder. Create and activate a virtual environment, then install the backend dependencies.

**Windows PowerShell:**

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS or Linux:**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 7. How to Run the Application

From the `backend` directory, run:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser. Flask serves both the frontend and the `/api/analyze` endpoint, so no separate frontend server or CORS setup is required. Stop the server with `Ctrl+C`.

## 8. How the Matching Algorithm Works

1. pypdf extracts selectable text from each PDF page and the parser normalizes whitespace.
2. `matcher.py` checks the resume and job description against a predefined list of skill names and aliases. Matching ignores letter case and checks phrase boundaries to reduce partial-word matches.
3. The job skills found in the catalog are compared with the detected resume skills. Matching skills are the intersection; missing skills are recognized job skills not found in the resume.
4. The score is `matched job skills / recognized job skills in the description * 100`, rounded to one decimal place. If no catalog skills are found in the job description, the score is 0% and the UI explains that there is no skill overlap to score.

This is a basic skill-match score, not a professional ATS score, a quality rating, or a prediction of interview success. The catalog and matching rules can miss synonyms, context, transferable experience, and skills outside the list.

To extend detection, add a `(display name, phrases)` entry to `SKILL_PATTERNS` in `backend/matcher.py`.

## 9. Example Usage

1. Choose a text-based PDF resume smaller than 8 MB.
2. Paste a job description containing requirements such as Python, SQL, or Machine Learning.
3. Select **Analyze resume** and review the score, matching and missing skills, suggestions, and extracted resume text.

The browser sends the PDF and description to Flask on the same machine. The server parses the request stream and does not save the PDF. The result includes extracted resume text so the user can inspect what the PDF parser read; this text is returned to that browser for the current response.

## 10. Future Improvements

- Add OCR for scanned/image-only PDF resumes.
- Add configurable skill aliases and support more domains.
- Improve keyword extraction with carefully evaluated NLP techniques.
- Add unit tests for parsing, boundaries, scoring, and invalid requests.
- Add an optional local-only export of results, with explicit privacy controls.
- Improve PDF size/page limits and production deployment configuration.

## 11. Limitations

- This is not a full ATS system and does not evaluate formatting, seniority, evidence quality, or hiring fit.
- Only skills in the built-in catalog are considered; unknown terms and many synonyms are missed.
- Phrase matching does not understand whether a skill is used positively, negatively, or in context.
- Image-only and scanned PDFs need OCR and are not supported by this version.
- PDF text extraction quality varies by document. Check the extracted text before relying on the comparison.
- The development server is intended for local learning, not public production deployment.