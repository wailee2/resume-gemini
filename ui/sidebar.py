# ui/sidebar.py
# Renders the Streamlit sidebar and collects all user configuration.

import streamlit as st


class SidebarRenderer:
    def render(self) -> dict:
        with st.sidebar:
            # API Key
            st.markdown('<span class="section-label">Configuration</span>', unsafe_allow_html=True)
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="AIza...",
            )
            st.markdown("---")

            #Candidate profile
            # These fields populate the contact header of the generated resume.
            st.markdown('<span class="section-label">Your Profile</span>', unsafe_allow_html=True)
            full_name = st.text_input("Full Name", placeholder="Jane Doe")
            email = st.text_input("Email", placeholder="jane@email.com")
            phone = st.text_input("Phone", placeholder="+1 555 000 0000")
            location = st.text_input("Location", placeholder="San Francisco, CA")
            linkedin = st.text_input("LinkedIn / GitHub", placeholder="linkedin.com/in/janedoe")
            st.markdown("---")

            # Experience level 
            st.markdown('<span class="section-label">Experience Level</span>', unsafe_allow_html=True)
            exp_level = st.selectbox(
                "",
                options=[
                    "Entry Level (0–2 yrs)",
                    "Mid Level (3–5 yrs)",
                    "Senior (6–10 yrs)",
                    "Lead / Principal (10+ yrs)",
                ],
            )
            
            #Writing tone
            tone = st.select_slider(
                "Writing Tone",
                options=["Conservative", "Professional", "Balanced", "Dynamic", "Bold"],
                value="Professional",
            )
            st.markdown("---")

            #Output options
            st.markdown('<span class="section-label">Output Options</span>', unsafe_allow_html=True)

            # Slider — how many interview questions to generate (5–20).
            n_questions = st.slider("Interview Questions", min_value=5, max_value=20, value=10)

            # Toggle — when enabled, the resume prompt gains ATS-specific instructions.
            ats_mode = st.toggle("ATS-Optimised Resume", value=True)

        # Return all values.
        return {
            "api_key": api_key,
            "full_name": full_name,
            "email": email or "",
            "phone": phone or "",
            "location": location or "",
            "linkedin": linkedin or "",
            "exp_level": exp_level,
            "tone": tone,
            "n_questions": n_questions,
            "ats_mode": ats_mode,
        }


def render_sidebar() -> dict:
    return SidebarRenderer().render()