import re               # Standard library regex module for pattern-based text substitution


class TextUtils:
    """
    Utility class that sanitises AI-generated text strings so they are safe
    to embed in a PDF rendered by FPDF2.

    FPDF2 uses the latin-1 (ISO 8859-1) character encoding internally, which
    means characters outside that range will cause encoding errors or silent
    replacement with '?' unless we normalise them first.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Sanitise AI-generated text for safe embedding in a PDF.

        Pipeline:
            1. Strip Markdown formatting markers (bold, italic, headings, rules).
            2. Replace common Unicode punctuation/symbols with ASCII equivalents.
            3. Encode to latin-1 and back, replacing anything still unrepresentable.

        Args:
            text: Raw string coming from the Gemini API response.

        Returns:
            A latin-1-safe, Markdown-free string ready for FPDF rendering.
        """

        # Strip Markdown markers
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)        # Remove **bold** markers, keeping only the inner text
        text = re.sub(r"\*(.+?)\*", r"\1", text)            # Remove *italic* markers, keeping only the inner text
        text = re.sub(r"#{1,6}\s*", "", text)               # Remove Markdown headings (e.g., # Heading), keeping only the text     
        text = re.sub(r"---+", "-" * 40, text)              # Replace Markdown horizontal rules (---) with line of dashes for visual separation

        # Unicode → ASCII mapping
        """
            Maps Unicode typographic characters that break latin-1 encoding to
            their closest ASCII equivalents.  Keys are literal Unicode code points.
        """
        replacements = {
            "\u2013": "-",      # En dash → hyphen-minus
            "\u2014": "-",      # Em dash → hyphen-minus
            "\u2018": "'",      # Left single quotation mark → apostrophe
            "\u2019": "'",      # Right single quotation mark → apostrophe
            "\u201c": '"',      # Left double quotation mark → double quotation mark
            "\u201d": '"',      # Right double quotation mark → double quotation mark
            "\u2022": "-",      # Bullet point •   → hyphen-minus
            "\u2026": "...",    # Horizontal ellipsis … → three dots
            "\u00a0": " ",      # Non-breaking space → regular space
            "\u2012": "-",      # Figure dash     → hyphen-minus
            "\u2015": "-",      # Horizontal bar  → hyphen-minus
            "\u00b7": "-",      # Middle dot ·     → hyphen-minus
            "\u25cf": "-",      # Black circle ●   → hyphen-minus
            "\u2192": "->",     # Rightwards arrow → arrow symbol
            "\u00e9": "e",      # é (e-acute) → lowercase e
            "\u00e8": "e",      # è (e-grave) → lowercase e
            "\u00ea": "e",      # ê (e-circumflex) → lowercase e
        }

        # Apply every mapping in a single pass over the replacement dictionary
        for unicode_char, ascii_equiv in replacements.items():
            text = text.replace(unicode_char, ascii_equiv)

        # Safe fallback for PDF rendering
        text = text.encode("latin-1", errors="replace").decode("latin-1")
        return text.strip()


def clean_text(text: str) -> str:
    """
    Thin module-level alias so callers can do `from helpers.text_utils import clean_text`
    without importing the class directly.
    """
    return TextUtils.clean_text(text)