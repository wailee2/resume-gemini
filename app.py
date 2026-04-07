import re
import streamlit as st

from helpers.text_utils import clean_text
from helpers.pdf_utils import build_pdf
from services.gemini_service import call_gemini
from ui.sidebar import render_sidebar
from ui.output import render_output


class ResumeGeneratorApp:
    def __init__(self):
        st.set_page_config(
            page_title="AI Resume Generator",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def _render_css(self):
        st.markdown(
            """
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

                /* ── Base reset ── */
                html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
                .main { background: #0c0e14; }
                [data-testid="stAppViewContainer"] { background: #0c0e14; }
                [data-testid="stSidebar"] { background: #111320; border-right: 1px solid #1e2236; }
                [data-testid="stHeader"] { background: transparent; }

                /* ── Headings ── */
                h1, h2, h3 {
                    font-family: 'Syne', sans-serif !important;
                    color: #f0f2ff !important;
                }

                /* ── Hero banner ── */
                .hero-header {
                    background: linear-gradient(135deg, #0d1117 0%, #161b2e 50%, #0d1117 100%);
                    border: 1px solid #1e2845;
                    border-radius: 16px;
                    padding: 40px 48px;
                    margin-bottom: 32px;
                    position: relative;
                    overflow: hidden;
                }
                .hero-header::before {
                    content: '';
                    position: absolute;
                    top: -60px; right: -60px;
                    width: 240px; height: 240px;
                    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
                    border-radius: 50%;
                }
                .hero-header::after {
                    content: '';
                    position: absolute;
                    bottom: -40px; left: -40px;
                    width: 180px; height: 180px;
                    background: radial-gradient(circle, rgba(20,184,166,0.12) 0%, transparent 70%);
                    border-radius: 50%;
                }
                .hero-title {
                    font-family: 'Syne', sans-serif;
                    font-size: 2.6rem;
                    font-weight: 800;
                    color: #f0f2ff;
                    margin: 0 0 6px 0;
                    letter-spacing: -0.5px;
                }
                .hero-sub {
                    font-family: 'DM Sans', sans-serif;
                    font-size: 1rem;
                    color: #6b7280;
                    font-weight: 300;
                    margin: 0;
                }
                .accent { color: #818cf8; }

                /* ── Section labels (small caps above inputs) ── */
                .section-label {
                    font-family: 'Syne', sans-serif;
                    font-size: 0.7rem;
                    font-weight: 700;
                    letter-spacing: 2.5px;
                    text-transform: uppercase;
                    color: #818cf8;
                    margin-bottom: 8px;
                    display: block;
                }

                /* ── Output cards ── */
                .output-card {
                    background: #111320;
                    border: 1px solid #1e2236;
                    border-radius: 12px;
                    padding: 28px 32px;
                    margin-bottom: 20px;
                    position: relative;
                }
                .output-card:hover { border-color: #2d3458; transition: border-color 0.2s; }
                .card-title {
                    font-family: 'Syne', sans-serif;
                    font-size: 0.75rem;
                    font-weight: 700;
                    letter-spacing: 2.5px;
                    text-transform: uppercase;
                    color: #818cf8;
                    margin-bottom: 16px;
                }

                /* ── Generation status pill ── */
                .status-pill {
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    background: rgba(20,184,166,0.12);
                    border: 1px solid rgba(20,184,166,0.3);
                    color: #14b8a6;
                    font-size: 0.75rem;
                    font-weight: 500;
                    padding: 4px 12px;
                    border-radius: 999px;
                    margin-bottom: 20px;
                }

                /* ── Form inputs ── */
                [data-testid="stTextInput"] input,
                [data-testid="stTextArea"] textarea,
                [data-testid="stSelectbox"] select {
                    background: #0c0e14 !important;
                    border: 1px solid #1e2236 !important;
                    border-radius: 8px !important;
                    color: #d1d5db !important;
                    font-family: 'DM Sans', sans-serif !important;
                }
                [data-testid="stTextInput"] input:focus,
                [data-testid="stTextArea"] textarea:focus {
                    border-color: #818cf8 !important;
                    box-shadow: 0 0 0 2px rgba(129,140,248,0.12) !important;
                }

                /* ── Primary action button ── */
                .stButton > button {
                    background: #818cf8 !important;
                    color: #0c0e14 !important;
                    font-family: 'Syne', sans-serif !important;
                    font-weight: 700 !important;
                    font-size: 0.85rem !important;
                    letter-spacing: 0.5px !important;
                    border: none !important;
                    border-radius: 8px !important;
                    padding: 10px 24px !important;
                    transition: all 0.2s !important;
                }
                .stButton > button:hover {
                    background: #6366f1 !important;
                    transform: translateY(-1px) !important;
                    box-shadow: 0 8px 20px rgba(99,102,241,0.3) !important;
                }

                /* ── Download button (outlined variant) ── */
                [data-testid="stDownloadButton"] > button {
                    background: transparent !important;
                    color: #818cf8 !important;
                    border: 1px solid #818cf8 !important;
                    font-family: 'Syne', sans-serif !important;
                    font-weight: 600 !important;
                    font-size: 0.8rem !important;
                    border-radius: 8px !important;
                    padding: 8px 20px !important;
                }
                [data-testid="stDownloadButton"] > button:hover {
                    background: rgba(129,140,248,0.1) !important;
                }

                /* ── Tab bar ── */
                [data-testid="stTabs"] [data-baseweb="tab-list"] {
                    background: transparent;
                    border-bottom: 1px solid #1e2236;
                    gap: 4px;
                }
                [data-testid="stTabs"] [data-baseweb="tab"] {
                    font-family: 'DM Sans', sans-serif !important;
                    font-size: 0.85rem !important;
                    color: #6b7280 !important;
                    padding: 8px 16px !important;
                    background: transparent !important;
                    border-radius: 6px 6px 0 0 !important;
                }
                [data-testid="stTabs"] [aria-selected="true"] {
                    color: #f0f2ff !important;
                    background: rgba(129,140,248,0.08) !important;
                    border-bottom: 2px solid #818cf8 !important;
                }

                /* ── Sidebar text ── */
                [data-testid="stSidebar"] .stMarkdown p { color: #9ca3af; font-size: 0.85rem; }
                [data-testid="stSidebar"] label        { color: #9ca3af !important; font-size: 0.82rem !important; }

                /* ── Horizontal rule ── */
                .divider { border: none; border-top: 1px solid #1e2236; margin: 20px 0; }

                /* ── Interview question cards ── */
                .iq-item {
                    background: #0c0e14;
                    border-left: 3px solid #818cf8;
                    border-radius: 0 8px 8px 0;
                    padding: 12px 16px;
                    margin-bottom: 10px;
                    color: #d1d5db;
                    font-size: 0.88rem;
                    line-height: 1.5;
                }

                /* ── Misc overrides ── */
                [data-testid="stSpinner"]   { color: #818cf8 !important; }
                [data-testid="stExpander"]  { border: 1px solid #1e2236 !important; border-radius: 10px !important; background: #111320 !important; }
                [data-testid="stExpander"] summary { color: #d1d5db !important; font-family: 'DM Sans', sans-serif !important; }
                [data-testid="stAlert"]     { background: rgba(129,140,248,0.08) !important; border: 1px solid rgba(129,140,248,0.25) !important; border-radius: 8px !important; color: #c7d2fe !important; }

                /* ── Pre-formatted resume / cover-letter text ── */
                .resume-content, .cl-content {
                    color: #c9cfe0;
                    font-size: 0.9rem;
                    line-height: 1.75;
                    white-space: pre-wrap;
                    font-family: 'DM Sans', sans-serif;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_hero(self):
        st.markdown(
            """
            <div class="hero-header">
                <p class="hero-title">AI <span class="accent">Resume</span> Generator 📄</p>
                <p class="hero-sub">Paste a job description → receive a tailored resume, cover letter & interview prep — powered by Gemini.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def run(self):
        self._render_css()

        sidebar_data = render_sidebar()
        self._render_hero()

        tab_input, tab_output = st.tabs(["✦  Input", "✦  Generated Output"])

        with tab_input:
            col1, col2 = st.columns([1, 1], gap="large")

            with col1:
                st.markdown('<span class="section-label">Job Description</span>', unsafe_allow_html=True)
                job_desc = st.text_area(
                    "",
                    height=300,
                    placeholder="Paste the full job description here — the more detail, the better the tailoring...",
                    key="jd",
                )

                st.markdown('<span class="section-label">Target Role & Company</span>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                job_title = c1.text_input("Job Title", placeholder="Senior Software Engineer", label_visibility="collapsed")
                company = c2.text_input("Company", placeholder="Acme Corp", label_visibility="collapsed")
                c1.caption("Job Title")
                c2.caption("Company Name")

            with col2:
                st.markdown('<span class="section-label">Your Background</span>', unsafe_allow_html=True)
                work_exp = st.text_area(
                    "",
                    height=140,
                    placeholder="Summarise your work experience: roles, companies, years, key achievements...",
                    key="work",
                )
                skills_raw = st.text_area(
                    "",
                    height=80,
                    placeholder="List key skills, technologies, certifications (comma-separated)...",
                    key="skills",
                )
                education = st.text_area(
                    "",
                    height=70,
                    placeholder="Degrees, institutions, graduation years...",
                    key="edu",
                )
                st.caption("Work Experience · Skills · Education")

            st.markdown("")
            generate_btn = st.button("⚡  Generate Resume Package", use_container_width=True)

        if generate_btn:
            missing = []
            if not sidebar_data["api_key"]:
                missing.append("Gemini API Key")
            if not sidebar_data["full_name"]:
                missing.append("Full Name")
            if not job_desc:
                missing.append("Job Description")
            if not work_exp:
                missing.append("Work Experience")

            if missing:
                st.warning(f"Please fill in: **{', '.join(missing)}**")
                st.stop()

            contact_block = (
                f"{sidebar_data['full_name']} | {sidebar_data['email']} | "
                f"{sidebar_data['phone']} | {sidebar_data['location']} | "
                f"{sidebar_data['linkedin']}"
            ).strip(" |")

            ats_note = (
                "Optimise the resume for ATS (Applicant Tracking Systems): use standard section headings, "
                "include keywords verbatim from the job description, avoid tables/columns."
                if sidebar_data["ats_mode"]
                else ""
            )

            resume_prompt = f"""
                You are an elite resume writer. Create a compelling, tailored resume.

                CANDIDATE DETAILS:
                - Name & Contact: {contact_block}
                - Experience Level: {sidebar_data['exp_level']}
                - Work History: {work_exp}
                - Skills: {skills_raw or 'Infer from work history'}
                - Education: {education or 'Not specified'}

                JOB DETAILS:
                - Title: {job_title or 'Not specified'}
                - Company: {company or 'Not specified'}
                - Description: {job_desc}

                INSTRUCTIONS:
                - Tone: {sidebar_data['tone']}
                - {ats_note}
                - Write a complete resume with sections: Summary, Work Experience, Skills, Education (and optional: Projects, Certifications).
                - Use strong action verbs and quantify achievements where possible.
                - Mirror language from the job description naturally.
                - Format cleanly using plain text with clear section headers in ALL CAPS.
                - Do NOT invent degrees, companies, or dates not provided.
                - Output ONLY the resume text, no preamble.
                """

            cl_prompt = f"""
                You are a world-class cover letter writer. Write a persuasive, authentic cover letter.

                CANDIDATE: {contact_block}
                ROLE: {job_title or 'the advertised role'} at {company or 'the company'}
                EXPERIENCE: {work_exp}
                SKILLS: {skills_raw or 'see experience'}
                TONE: {sidebar_data['tone']}

                JOB DESCRIPTION:
                {job_desc}

                INSTRUCTIONS:
                - 3-4 paragraphs: compelling opening, 2 body paragraphs (match experience to JD requirements), strong close.
                - Sound like a real human being — avoid buzzword soup.
                - Reference specific aspects of the job description.
                - End with a clear call-to-action.
                - Output ONLY the cover letter text, no preamble.
                """

            iq_prompt = f"""
                Generate exactly {sidebar_data['n_questions']} high-quality interview questions for this role.

                ROLE: {job_title or 'the role'} at {company or 'the company'}
                JOB DESCRIPTION: {job_desc}
                EXPERIENCE LEVEL: {sidebar_data['exp_level']}

                Include a good mix of:
                - Technical / role-specific questions
                - Behavioural (STAR) questions
                - Situational questions
                - Culture / motivation questions

                Format: Return ONLY a numbered list (1. Question text). No preamble, no explanations.
                """

            with tab_output:
                st.markdown(
                    '<div class="status-pill">⚡ Generating with Gemini 2.5 Flash</div>',
                    unsafe_allow_html=True,
                )
                prog = st.progress(0, text="Crafting your resume...")

                try:
                    resume_text = call_gemini(sidebar_data["api_key"], resume_prompt)
                    prog.progress(33, text="Writing cover letter...")

                    cl_text = call_gemini(sidebar_data["api_key"], cl_prompt)
                    prog.progress(66, text="Preparing interview questions...")

                    iq_raw = call_gemini(sidebar_data["api_key"], iq_prompt, temperature=0.8)
                    prog.progress(100, text="Done!")

                except Exception as e:
                    prog.empty()
                    st.error(f"Gemini API error: {e}")
                    st.stop()

                prog.empty()

            iq_lines = [
                re.sub(r"^\d+[\.\)]\s*", "", line).strip()
                for line in iq_raw.strip().split("\n")
                if line.strip() and re.match(r"^\d+", line.strip())
            ]

            st.session_state["resume"] = resume_text
            st.session_state["cl"] = cl_text
            st.session_state["questions"] = iq_lines
            st.session_state["iq_raw"] = iq_raw
            st.session_state["name"] = sidebar_data["full_name"]
            st.session_state["generated"] = True

        with tab_output:
            render_output(build_pdf, clean_text)


if __name__ == "__main__":
    ResumeGeneratorApp().run()