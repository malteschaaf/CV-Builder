import sys
from pathlib import Path

import streamlit as st
from streamlit_ace import st_ace

# Add project root to sys.path so we can import from utils without issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.markdown_processor import convert_md_to_pdf, preprocess_markdown

# -----------------------------------------------------------------------------
# Constants and Paths
# -----------------------------------------------------------------------------

# Define template paths
TEMPLATE_PATHS = {
    "Modern": Path("templates/modern.tex"),
    "Harvard": Path("templates/harvard.tex"),
}

# Paths to required files
inline_lua_filter_path = Path("filters/inline_dates.lua")
columns_lua_filter_path = Path("filters/columns.lua")
default_cv_path = Path("examples/default.md")

# -----------------------------------------------------------------------------
# Streamlit App Setup
# -----------------------------------------------------------------------------

st.set_page_config(page_title="CV Creator", layout="wide")
st.title("📄 CV Creator (Markdown → PDF)")
st.caption(
    "Upload or edit your Markdown CV and export a formatted PDF via Pandoc + LaTeX template."
)
st.divider()

# -----------------------------------------------------------------------------
# File Existence Check
# -----------------------------------------------------------------------------

# Ensure required files exist
for path, desc in [
    (inline_lua_filter_path, "Inline lua filter"),
    (columns_lua_filter_path, "Columns lua filter"),
    (default_cv_path, "Default CV markdown"),
]:
    if not path.exists():
        st.error(f"{desc} not found at {path}.")
        st.stop()

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------

if "md_text" not in st.session_state:
    st.session_state.md_text = default_cv_path.read_text(encoding="utf-8")

if "template_name" not in st.session_state:
    st.session_state.template_name = st.session_state.get(
        "active_template", "Modern"
    )  # UI state

if "active_template" not in st.session_state:
    st.session_state.active_template = "Modern"  # app state

if "custom_template_tex" not in st.session_state:
    st.session_state.custom_template_tex = None

if "custom_lua_filters" not in st.session_state:
    st.session_state.custom_lua_filters = {
        "columns": True,
        "inline_dates": True,
    }

if "pdf_generated" not in st.session_state:
    st.session_state.pdf_generated = False
    st.session_state.pdf_bytes = None

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------


def get_template_options():
    options = list(TEMPLATE_PATHS.keys())
    if st.session_state.custom_template_tex is not None:
        options.append("Custom")
    return options


def get_active_template_path():
    if st.session_state.active_template == "Custom":
        temp_path = Path("temp_custom_template.tex")
        temp_path.write_text(st.session_state.custom_template_tex, encoding="utf-8")
        return temp_path
    else:
        return TEMPLATE_PATHS[st.session_state.active_template]


def generate_pdf(
    md_text, columns_lua_filter_path, inline_lua_filter_path, template_path, rerun=True
):
    """
    Generates a PDF from Markdown text and updates the state in st.session_state.

    Args:
        md_text (str): The Markdown text to be converted into a PDF.
        columns_lua_filter_path (str): Path to the Lua filter for columns.
        inline_lua_filter_path (str): Path to the Lua filter for inline data.
        template_path (str): Path to the LaTeX template.
        rerun (bool): Whether to trigger a rerun after generating the PDF (default: True).

    Returns:
        None: Updates the state in st.session_state and triggers a rerun to display the PDF preview.
    """
    try:
        # Prepare Markdown
        md_for_pandoc = preprocess_markdown(md_text)

        # Generate PDF using Lua filters
        lua_filters = [columns_lua_filter_path, inline_lua_filter_path]
        pdf_bytes = convert_md_to_pdf(md_for_pandoc, template_path, lua_filters)

        # Update session state
        st.session_state.pdf_generated = True
        st.session_state.pdf_bytes = pdf_bytes

        # Trigger a rerun to display the PDF preview
        if rerun:
            st.rerun()
    except Exception as e:
        st.error("Failed to generate PDF")
        st.code(str(e))


def on_template_change():
    st.session_state.active_template = st.session_state.template_name
    generate_pdf(
        st.session_state.md_text,
        columns_lua_filter_path,
        inline_lua_filter_path,
        get_active_template_path(),
        rerun=False,
    )


# -----------------------------------------------------------------------------
# Markdown Editor and PDF Preview
# -----------------------------------------------------------------------------

editor_col, preview_col = st.columns([1, 1], gap="medium")

# Left column: Markdown editor
with editor_col:
    st.subheader("Markdown Editor")

    # Text area for Markdown editing
    st.session_state.md_text = st.text_area(
        "CV Markdown",
        st.session_state.md_text,
        height=600,
        key="cv_editor",
        label_visibility="collapsed",
    )

    uploaded = st.file_uploader(
        "Upload cv.md", type=["md", "markdown", "txt"], label_visibility="collapsed"
    )

    # File uploader for Markdown files
    if uploaded is not None:
        st.session_state.md_text = uploaded.read().decode("utf-8")
        st.rerun()

    # Download button for Markdown
    st.download_button(
        label="⬇️ Download Markdown",
        data=st.session_state.md_text.encode("utf-8"),
        file_name="cv.md",
        mime="text/markdown",
        use_container_width=True,
    )

# Right column: PDF Preview
with preview_col:
    st.subheader("PDF Preview")

    if not st.session_state.pdf_generated:
        # Generate PDF button
        if st.button("🚀 Generate PDF", type="primary", use_container_width=True):
            generate_pdf(
                st.session_state.md_text,
                columns_lua_filter_path,
                inline_lua_filter_path,
                get_active_template_path(),
            )
    else:
        # Display PDF preview
        st.pdf(st.session_state.pdf_bytes, height=600)

        st.success("PDF generated successfully.")

        # Regenerate PDF button
        if st.button("🚀 Regenerate PDF", type="primary", use_container_width=True):
            generate_pdf(
                st.session_state.md_text,
                columns_lua_filter_path,
                inline_lua_filter_path,
                get_active_template_path(),
            )

        # Download button for PDF
        st.download_button(
            label="⬇️ Download CV PDF",
            data=st.session_state.pdf_bytes,
            file_name="cv.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# -----------------------------------------------------------------------------
# Template & Build Settings
# -----------------------------------------------------------------------------

st.divider()
st.subheader("Template & Build Settings")

template_col, settings_col = st.columns([1, 2])

# Template selection
with template_col:
    st.selectbox(
        "Template",
        options=get_template_options(),
        key="template_name",  # Bind the selectbox to a session state key
        on_change=on_template_change,
    )

# Template editor
with st.expander("Edit template", expanded=False):
    template_code = get_active_template_path().read_text(encoding="utf-8")

    if st.session_state.active_template == "Custom":
        # Editable text area for custom template
        st.session_state.custom_template_tex = st_ace(
            value=template_code,
            language="latex",
            theme="monokai",
            height=500,
            key="custom_template_editor",
        )

        st.session_state.custom_lua_filters["columns"] = st.checkbox(
            "columns.lua",
            value=st.session_state.custom_lua_filters["columns"],
        )

        st.session_state.custom_lua_filters["inline_dates"] = st.checkbox(
            "inline_dates.lua",
            value=st.session_state.custom_lua_filters["inline_dates"],
        )

        st.download_button(
            label="⬇️ Download custom LaTeX template",
            data=st.session_state.custom_template_tex.encode("utf-8"),
            file_name="custom_template.tex",
            mime="text/x-tex",
            use_container_width=True,
        )

    else:
        # Read-only template
        st.code(template_code, language="latex", height=500)

        # Edit as custom template button
        if st.button("Edit as custom template"):
            st.session_state.custom_template_tex = template_code
            st.session_state.active_template = "Custom"

            # reset widget safely on next run
            st.session_state.pop("template_name", None)
            st.rerun()

# -----------------------------------------------------------------------------
# Export Section
# -----------------------------------------------------------------------------

st.divider()
st.subheader("Export")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    st.download_button(
        label="⬇️ Download PDF",
        type="primary",
        data=st.session_state.pdf_bytes if st.session_state.pdf_generated else b"",
        file_name="cv.pdf",
        mime="application/pdf",
        use_container_width=True,
        disabled=True if not st.session_state.pdf_generated else False,
    )


with export_col2:
    st.download_button(
        label="⬇️ Download TEX",
        data=st.session_state.pdf_bytes if st.session_state.pdf_generated else b"",
        file_name="cv.pdf",
        mime="application/pdf",
        use_container_width=True,
        disabled=True if not st.session_state.pdf_generated else False,
    )

with export_col3:
    st.download_button(
        label="⬇️ Download Markdown",
        data=st.session_state.pdf_bytes if st.session_state.pdf_generated else b"",
        file_name="cv.pdf",
        mime="application/pdf",
        use_container_width=True,
        disabled=True if not st.session_state.pdf_generated else False,
    )

# -----------------------------------------------------------------------------
# FAQ Section
# -----------------------------------------------------------------------------

st.divider()
st.subheader("FAQ")

with st.expander("Why is my PDF not generating?", expanded=False):
    st.markdown(
        """
        Common issues:
        - Invalid Markdown syntax (check for unclosed tags, etc.)
        - Missing required files (Lua filters, template)
        - Pandoc or LaTeX errors (check console for details)
        """
    )

with st.expander("How do I customize the template?", expanded=False):
    st.markdown(
        """
        You can upload your own LaTeX template or edit the existing ones. Make sure to follow Pandoc's template syntax.
        """
    )

with st.expander("Can I use this for non-CV documents?", expanded=False):
    st.markdown(
        """
        Yes! The tool is designed for CVs but can be used to convert any Markdown document to PDF using your chosen template and filters.
        """
    )

with st.expander("How does the AI optimization work?", expanded=False):
    st.markdown(
        """
        The AI optimization will analyze your CV and a provided job description to suggest improvements. It will never add new experience but can help rephrase and reorganize content for better relevance.
        """
    )

with st.expander("I found a bug or have a feature request!", expanded=False):
    st.markdown(
        """
        Please open an issue on our GitHub repository with details and screenshots if possible. We appreciate your feedback!
        """
    )

with st.expander("How can I contribute?", expanded=False):
    st.markdown(
        """
        Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Check our contribution guidelines for more details.
        """
    )

with st.expander("What are the limitations of this tool?", expanded=False):
    st.markdown(
        """
        - The PDF generation relies on Pandoc and LaTeX, so complex templates may require adjustments.
        - AI optimization is in early stages and may not always produce perfect results. Always review changes before applying.
        - The tool is designed for CVs but can be used for other documents with the right template and filters.
        """
    )
