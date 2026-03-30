# 📄 AI Resume Generator

A Streamlit application that generates tailored resumes, cover letters, and interview prep packages from any job description — powered by Google Gemini.

---

## Features

| Feature | Detail |
|---|---|
| **AI Resume** | Tailored to the job description, ATS-optimised |
| **Cover Letter** | Persuasive, tone-adjustable, human-sounding |
| **Interview Prep** | 5–20 role-specific questions (technical + behavioural) |
| **PDF Export** | One-click download of the full career package |
| **Customisation** | Tone slider, experience level, ATS mode toggle |

---

## Setup

### 1. Clone / download the project
```bash
git clone https://github.com/wailee2/resume-gemini && cd resume-gemini
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate     # Mac/Linux: source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **Create API key**
3. Copy the key — it starts with `AIza...`

---

## Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Usage

1. **Sidebar** → Paste your Gemini API key and fill in your profile
2. **Input tab** → Paste the job description + your background
3. Hit **📄 Generate Resume Package**
4. **Output tab** → Review resume, cover letter, and interview questions
5. Click **⬇ Download Full PDF** to save everything

---

## Project Structure

```
ai-resume-generator/
│
├── app.py              # Main Streamlit application
├── helpers/
│   ├── text_utils.py
│   └── pdf_utils.py
├── services/
│   └── gemini_service.py
├── ui/
│   ├── sidebar.py
│   └── output.py
└── requirements.txt    # Python dependencies
└── README.md
```

---

## Dependencies

- `streamlit` — UI framework
- `google-genai` — Gemini API client
- `fpdf2` — PDF generation

---

## Notes

- The app uses **Gemini 2.5 Flash** (fast + cost-effective)
- No data is stored — all generation happens in-session
- ATS mode mirrors job description keywords for applicant tracking systems
