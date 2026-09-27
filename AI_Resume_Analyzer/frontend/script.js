const form = document.querySelector("#analysis-form");
const resumeInput = document.querySelector("#resume");
const jobDescriptionInput = document.querySelector("#job-description");
const fileName = document.querySelector("#file-name");
const characterCount = document.querySelector("#character-count");
const analyzeButton = document.querySelector("#analyze-button");
const formMessage = document.querySelector("#form-message");
const loadingMessage = document.querySelector("#loading-message");
const resultsSection = document.querySelector("#results");

resumeInput.addEventListener("change", () => {
  fileName.textContent = resumeInput.files[0]?.name || "Choose a PDF file, up to 8 MB";
});

jobDescriptionInput.addEventListener("input", () => {
  const count = jobDescriptionInput.value.length;
  characterCount.textContent = `${count.toLocaleString()} ${count === 1 ? "character" : "characters"}`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage("");

  const resume = resumeInput.files[0];
  const jobDescription = jobDescriptionInput.value.trim();

  if (!resume) {
    showMessage("Choose a PDF resume to continue.");
    resumeInput.focus();
    return;
  }
  if (!resume.name.toLowerCase().endsWith(".pdf")) {
    showMessage("The resume must be a PDF file.");
    resumeInput.focus();
    return;
  }
  if (resume.size > 8 * 1024 * 1024) {
    showMessage("The PDF must be smaller than 8 MB.");
    resumeInput.focus();
    return;
  }
  if (!jobDescription) {
    showMessage("Paste a job description to continue.");
    jobDescriptionInput.focus();
    return;
  }

  const formData = new FormData();
  formData.append("resume", resume);
  formData.append("job_description", jobDescription);
  setLoading(true);

  try {
    const response = await fetch("/api/analyze", { method: "POST", body: formData });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "The analysis could not be completed.");
    }
    renderResults(result);
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    showMessage(error.message || "Could not reach the server. Make sure Flask is running and try again.");
  } finally {
    setLoading(false);
  }
});

function showMessage(message) {
  formMessage.textContent = message;
  formMessage.hidden = !message;
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.querySelector("span:first-child").textContent = isLoading ? "Analyzing..." : "Analyze resume";
  loadingMessage.hidden = !isLoading;
}

function renderResults(result) {
  const score = Number(result.match_percentage) || 0;
  document.querySelector("#score-value").textContent = `${score}%`;
  document.querySelector("#score-ring").style.setProperty("--score", `${score}%`);
  document.querySelector("#score-ring").setAttribute("aria-label", `${score} percent skill match`);
  document.querySelector("#score-explanation").textContent = result.important_job_keywords.length
    ? `${result.matched_skills.length} of ${result.important_job_keywords.length} recognized job skills found in your resume.`
    : "No catalog skills were detected in this job description, so there is no skill overlap to score.";

  renderList("#matched-skills", result.matched_skills, "#matched-empty");
  renderList("#missing-skills", result.missing_skills, "#missing-empty");
  renderList("#job-keywords", result.important_job_keywords, "#keywords-empty");
  renderList("#resume-skills", result.detected_resume_skills, "#resume-skills-empty");
  renderList("#suggestions", result.suggestions);
  document.querySelector("#resume-text").textContent = result.resume_text || "No text was extracted.";

  resultsSection.hidden = false;
}

function renderList(selector, items, emptySelector) {
  const list = document.querySelector(selector);
  list.replaceChildren();
  for (const item of items || []) {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    list.append(listItem);
  }
  if (emptySelector) {
    document.querySelector(emptySelector).hidden = Boolean(items?.length);
    list.hidden = !items?.length;
  }
}