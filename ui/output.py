from typing import Callable
import streamlit as st


class OutputRenderer:
    def render(self, build_pdf: Callable, clean_text: Callable) -> None:
        if not st.session_state.get("generated"):
            st.markdown(
                """
                <div style="text-align:center; padding: 80px 0; color: #374151;">
                    <div style="font-size: 3rem; margin-bottom: 12px;">📄</div>
                    <p style="font-family: 'Syne', sans-serif; font-size: 1.1rem; color: #4b5563;">
                        Fill in the Input tab and hit
                        <strong style="color: #818cf8;">Generate</strong>
                        to create your resume package.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        resume_text = st.session_state["resume"]
        cl_text = st.session_state["cl"]
        iq_lines = st.session_state["questions"]
        name_val = st.session_state["name"]

        pdf_bytes = build_pdf(name_val, resume_text, cl_text, iq_lines)
        fname = f"{name_val.replace(' ', '_')}_Career_Package.pdf"

        dl_col, _, _ = st.columns([1, 2, 1])
        dl_col.download_button(
            label="⬇  Download Full PDF",
            data=pdf_bytes,
            file_name=fname,
            mime="application/pdf",
            use_container_width=True,
        )
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        r_col, cl_col = st.columns(2, gap="large")

        with r_col:
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">📄 Tailored Resume</p>', unsafe_allow_html=True)
            st.text_area("", value=resume_text, height=520, key="resume_out", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)

        with cl_col:
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">✉  Cover Letter</p>', unsafe_allow_html=True)
            st.text_area("", value=cl_text, height=520, key="cl_out", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">🎯 Suggested Interview Questions</p>', unsafe_allow_html=True)

        if iq_lines:
            cols = st.columns(2)
            for i, question in enumerate(iq_lines):
                with cols[i % 2]:
                    st.markdown(
                        f'<div class="iq-item"><strong style="color:#818cf8">{i + 1}.</strong> {question}</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No questions parsed — check the raw output below.")
            st.text(st.session_state.get("iq_raw", ""))

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("↺  Regenerate", use_container_width=False):
            st.session_state["generated"] = False
            st.rerun()


def render_output(build_pdf: Callable, clean_text: Callable) -> None:
    return OutputRenderer().render(build_pdf, clean_text)