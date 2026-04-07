from fpdf import FPDF                       # FPDF2 library for programmatic PDF generation
from helpers.text_utils import TextUtils    # Our custom text sanitiser for PDF-safe output

class PDFBuilder:

    """
    Responsible for assembling a multi-section PDF document that bundles
    the candidate's tailored resume, cover letter, and interview questions
    into a single downloadable file.
    """

    @staticmethod
    def build_pdf(name: str, resume: str, cover_letter: str, questions: list[str]) -> bytes:
        """
        Build and return the complete PDF as raw bytes.

        Args:
            name:         Candidate's full name (used for page metadata / future headers).
            resume:       AI-generated resume text.
            cover_letter: AI-generated cover letter text.
            questions:    List of interview question strings.

        Returns:
            bytes: The rendered PDF binary, ready to pass to Streamlit's download_button.
        """

        # Initialise document
        pdf = FPDF()                                    # Create a blank FPDF document object
        pdf.set_auto_page_break(auto=True, margin=18)   # Auto page-break 18 pt from the bottom
        pdf.add_page()                                  # Start with the first (resume) page

        # Inner helper functions for consistent styling of section headers and body text
        def section_header(title: str) -> None:
            """
            Renders a styled section banner (dark fill + indigo border + uppercase label)
            that visually separates each content section inside the PDF.
            """
            pdf.set_fill_color(20, 22, 40)      # Deep navy background for the header cell
            pdf.set_draw_color(100, 100, 200)   # Soft indigo border colour
            pdf.set_line_width(0.5)             # Thin border line so it looks refined
            pdf.set_x(14)                       # Indent 14 pt from the left margin
            pdf.set_font("Helvetica", "B", 10)  # Bold Helvetica at 10 pt for the label
            pdf.set_text_color(180, 190, 255)   # Light lavender text on the dark background
            # Draw a filled cell with left + bottom borders, then move to the next line
            pdf.cell(182, 8, f"  {title.upper()}", border="LB", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)                           # Small breathing room below the header

        # Inner helper: body_text
        def body_text(content: str) -> None:
            """
            Renders multi-line body copy with smart detection for ALL-CAPS sub-headings
            so that internal resume section titles (e.g. "WORK EXPERIENCE") receive
            distinct styling without manual tagging.
            """
            pdf.set_font("Helvetica", "", 9.5)  # Regular Helvetica for body prose
            pdf.set_text_color(50, 50, 60)      # Dark charcoal — readable on white

            # Sanitise the AI-generated text (strip Markdown, fix Unicode) before rendering
            cleaned = TextUtils.clean_text(content)

            # Iterate over every line in the cleaned content
            for line in cleaned.split("\n"):
                line = line.strip()             # Remove leading/trailing whitespace

                if not line:
                    # Blank line → insert a small vertical gap instead of an empty cell
                    pdf.ln(3)
                    continue

                # Detect ALL-CAPS sub-headings (e.g. "WORK EXPERIENCE", "SKILLS")
                # — short length guard prevents false positives on long shouted sentences
                if line.isupper() and len(line) < 50:
                    # Render sub-heading in bold indigo
                    pdf.set_font("Helvetica", "B", 9.5)
                    pdf.set_text_color(80, 80, 160)     # Medium indigo for visual hierarchy
                    pdf.set_x(14)                       # Align to the same left indent as the header
                    pdf.multi_cell(182, 5.5, line)      # Allow text to wrap across multiple lines
                    # Reset back to regular body style after the sub-heading
                    pdf.set_font("Helvetica", "", 9.5)
                    pdf.set_text_color(50, 50, 60)
                else:
                    # Standard body line — just indent and render
                    pdf.set_x(14)
                    pdf.multi_cell(182, 5.5, line)      # 5.5 pt line height keeps it compact

            pdf.ln(4)                                   # Extra space after each content block

        # Page 1: Resume
        section_header("Resume")                        # Draw the "RESUME" section banner
        body_text(resume)                               # Render the full resume text below it
        pdf.add_page()                                  # Force a clean page break before the cover letter

        # Page 2: Cover Letter
        section_header("Cover Letter")                  # Draw the "COVER LETTER" section banner
        body_text(cover_letter)                         # Render the full cover letter text below it
        pdf.add_page()                                  # Force a clean page break before the interview questions

        # Page 3: Interview Questions
        section_header("Suggested Interview Questions")
        pdf.ln(2)                                       # A little extra space before the first question

        # Enumerate from 1 so the displayed number matches the list position
        for i, question in enumerate(questions, start=1):
            # Draw a small tinted square as the question number badge
            pdf.set_fill_color(230, 232, 255)
            pdf.set_x(14)
            pdf.set_font("Helvetica", "B", 8.5)
            pdf.set_text_color(60, 60, 150)
            pdf.cell(6, 6, str(i), fill=True)

            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(40, 40, 55)
            pdf.multi_cell(176, 6, f"  {TextUtils.clean_text(question)}")
            pdf.ln(2)

        # Serialise the in-memory PDF to raw bytes and return
        return bytes(pdf.output())


# Module-level wrapper
def build_pdf(name: str, resume: str, cover_letter: str, questions: list[str]) -> bytes:
    return PDFBuilder.build_pdf(name, resume, cover_letter, questions)