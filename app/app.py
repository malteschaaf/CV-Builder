import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Add project root to sys.path so we can import from utils without issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.markdown_processor import convert_md_to_pdf, preprocess_markdown

# Streamlit app setup
st.set_page_config(page_title="CV Creator", layout="wide")
st.title("📄 CV Creator (Markdown → PDF)")
st.write(
    "Upload or edit your Markdown CV and export a formatted PDF via Pandoc + LaTeX template."
)

# Paths to required files
template_path = Path("templates/template.tex")
inline_lua_filter_path = Path("filters/inline_dates.lua")
columns_lua_filter_path = Path("filters/columns.lua")
default_cv_path = Path("examples/default.md")

# Check required files exist
for path, desc in [
    (template_path, "LaTeX template"),
    (inline_lua_filter_path, "Inline lua filter"),
    (columns_lua_filter_path, "Columns lua filter"),
    (default_cv_path, "Default CV markdown"),
]:
    if not path.exists():
        st.error(f"{desc} not found at {path}.")
        st.stop()

# Load default CV markdown from file
default_md = default_cv_path.read_text(encoding="utf-8")

# Use session state so uploads + edits behave correctly
if "md_text" not in st.session_state:
    st.session_state.md_text = default_md

col1, col2 = st.columns([1, 1])

# Left column: Markdown editor
with col1:
    st.subheader("1) Edit CV Markdown")
    st.caption(
        "Edit your CV in Markdown. Use headings (#, ##, ###) for structure and '-' for bullet points. "
        "You can upload an existing file or download your current Markdown anytime."
    )
    st.space(size="medium")

    # Markdown editor
    st.session_state.md_text = st.text_area(
        "CV Markdown", st.session_state.md_text, height=700, key="cv_editor"
    )

    # Buttons row under the editor
    btn_col1, btn_col2 = st.columns([1, 1])

    # File uploader
    with btn_col1:
        uploaded = st.file_uploader(
            "Upload cv.md", type=["md", "markdown", "txt"], label_visibility="collapsed"
        )

        # If user uploads a file, overwrite editor content
        if uploaded is not None:
            st.session_state.md_text = uploaded.read().decode("utf-8")
            st.rerun()

    # Download button
    with btn_col2:
        st.download_button(
            label="⬇️ Download Markdown",
            data=st.session_state.md_text.encode("utf-8"),
            file_name="cv.md",
            mime="text/markdown",
            use_container_width=True,
        )

# Right column: PDF export
with col2:
    st.subheader("2) Export PDF")

    if st.button("🚀 Generate PDF", type="primary", use_container_width=True):
        try:
            md_for_pandoc = preprocess_markdown(st.session_state.md_text)

            lua_filters = [columns_lua_filter_path, inline_lua_filter_path]

            pdf_bytes = convert_md_to_pdf(md_for_pandoc, template_path, lua_filters)

            st.space(size="stretch")
            st.success("PDF generated successfully.")

            # PDF Preview
            st.pdf(pdf_bytes, height=800)

            st.download_button(
                label="⬇️ Download CV PDF",
                data=pdf_bytes,
                file_name="cv.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as e:
            st.error("Failed to generate PDF")
            st.code(str(e))
