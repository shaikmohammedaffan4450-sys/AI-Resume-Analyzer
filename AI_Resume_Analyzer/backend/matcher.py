"""Rule-based skill matching for resumes and job descriptions."""

import re
from collections.abc import Iterable


# Add skills here as (display name, phrases to recognize) pairs.
SKILL_PATTERNS = [
    ("Python", ("Python",)),
    ("Java", ("Java",)),
    ("C", ("C",)),
    ("C++", ("C++", "C plus plus")),
    ("JavaScript", ("JavaScript", "JS")),
    ("TypeScript", ("TypeScript",)),
    ("HTML", ("HTML",)),
    ("CSS", ("CSS",)),
    ("SQL", ("SQL",)),
    ("MySQL", ("MySQL",)),
    ("PostgreSQL", ("PostgreSQL",)),
    ("MongoDB", ("MongoDB",)),
    ("Flask", ("Flask",)),
    ("Django", ("Django",)),
    ("React", ("React",)),
    ("Node.js", ("Node.js", "Node JS")),
    ("Git", ("Git",)),
    ("GitHub", ("GitHub",)),
    ("Docker", ("Docker",)),
    ("AWS", ("AWS", "Amazon Web Services")),
    ("Machine Learning", ("Machine Learning",)),
    ("Deep Learning", ("Deep Learning",)),
    ("Artificial Intelligence", ("Artificial Intelligence",)),
    ("Data Science", ("Data Science",)),
    ("Data Analysis", ("Data Analysis",)),
    ("Computer Vision", ("Computer Vision",)),
    ("Natural Language Processing", ("Natural Language Processing", "NLP")),
    ("TensorFlow", ("TensorFlow",)),
    ("PyTorch", ("PyTorch",)),
    ("Scikit-learn", ("Scikit-learn", "Scikit learn")),
    ("Keras", ("Keras",)),
    ("Pandas", ("Pandas",)),
    ("NumPy", ("NumPy",)),
    ("Power BI", ("Power BI",)),
    ("Tableau", ("Tableau",)),
    ("REST API", ("REST API", "RESTful API")),
    ("FastAPI", ("FastAPI",)),
]


def _compile_skill_pattern(phrases: Iterable[str]) -> re.Pattern[str]:
    """Match whole skill phrases without matching inside longer words."""
    alternatives = "|".join(re.escape(phrase) for phrase in phrases)
    return re.compile(rf"(?<![A-Za-z0-9_+#])(?:{alternatives})(?![A-Za-z0-9_+#])", re.IGNORECASE)


COMPILED_SKILLS = [
    (name, _compile_skill_pattern(phrases)) for name, phrases in SKILL_PATTERNS
]


def detect_skills(text: str) -> list[str]:
    """Return recognized skills in the order defined by the skill catalog."""
    return [name for name, pattern in COMPILED_SKILLS if pattern.search(text)]


def analyze_resume(resume_text: str, job_description: str) -> dict[str, object]:
    """Compare recognized job skills against skills found in resume text."""
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_description)
    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    # This is a transparent skill overlap, not a professional ATS score.
    match_percentage = round(len(matched_skills) / len(job_skills) * 100, 1) if job_skills else 0.0

    suggestions = _make_suggestions(job_skills, matched_skills, missing_skills)
    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "detected_resume_skills": resume_skills,
        "important_job_keywords": job_skills,
        "suggestions": suggestions,
    }


def _make_suggestions(
    job_skills: list[str], matched_skills: list[str], missing_skills: list[str]
) -> list[str]:
    """Create practical suggestions from the detected skill overlap."""
    if not job_skills:
        return [
            "No skills from the built-in skill list were recognized in the job description. Add relevant terms to the skill catalog to improve this comparison."
        ]

    suggestions = []
    if missing_skills:
        missing_list = ", ".join(missing_skills[:6])
        suggestions.append(
            f"If you have hands-on experience with {missing_list}, make that experience easier to find in your resume."
        )
    if matched_skills:
        suggestions.append(
            "Support matching skills with a project, responsibility, or measurable result instead of listing skills alone."
        )
    suggestions.append(
        "Tailor your summary and project descriptions to the role, and keep every claim accurate."
    )
    return suggestions