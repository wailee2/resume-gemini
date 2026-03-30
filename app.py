import streamlit as st

class ResumeGeneratorApp:
    def __init__(self):
        st.set_page_config(
            page_title="AI Resume Generator",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self._render_css()

    def _render_css(self):
        st.markdown(
            """
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

                /* Base reset */
                html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
                .main { background: #0c0e14; }
                [data-testid="stAppViewContainer"] { background: #0c0e14; }
                [data-testid="stSidebar"] { background: #111320; border-right: 1px solid #1e2236; }
                
                /* Custom Hero Styling */
                .hero-header {
                    background: linear-gradient(135deg, #0d1117 0%, #161b2e 50%, #0d1117 100%);
                    border: 1px solid #1e2845;
                    border-radius: 16px;
                    padding: 40px 48px;
                    margin-bottom: 32px;
                }
                .hero-title {
                    font-family: 'Syne', sans-serif;
                    font-size: 2.6rem;
                    font-weight: 800;
                    color: #f0f2ff;
                }
                .accent { color: #818cf8; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_hero(self):
        st.markdown(
            """
            <div class="hero-header">
              <p class="hero-title">AI <span class="accent">Resume</span> Generator 📄</p>
              <p class="hero-sub">Tailored resumes & interview prep — powered by Gemini.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def run(self):
        self._render_hero()
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="section-label">Input Data</p>', unsafe_allow_html=True)
            st.text_area("Paste Job Description here...", height=200)

if __name__ == "__main__":
    app = ResumeGeneratorApp()
    app.run()