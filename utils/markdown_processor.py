"""Module for preprocessing markdown and converting it to PDF using Pandoc."""

import tempfile
from pathlib import Path

import pypandoc


def preprocess_markdown(md: str) -> str:
    """
    Correctly format Markdown by inserting blank lines between sections,
    while preserving bullet lists, blockquotes, and metadata blocks.

    Args:
        md: Input markdown as a string.

    Returns:
        Preprocessed markdown with proper spacing.
    """
    lines = md.splitlines()
    out = []
    prev = ""  # Tracks if the previous line was non-empty

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("---") and (not out or out[-1].strip() == "---"):
            # Handle metadata block delimiters
            out.append(line)
            prev = ""
            continue

        # Preserve empty lines as they are
        if not stripped_line:
            out.append(line)
            prev = ""
            continue

        # Check if the current line is part of a list or blockquote
        if stripped_line.startswith(("-", "*", "+", ">")):
            if prev and prev != stripped_line[0]:
                out.append("")
            out.append(line)
            prev = stripped_line[0]
            continue

        # Check if the current line is a heading
        if stripped_line.startswith("#"):
            # Add a blank line before the heading if the previous line is non-empty
            out.append("") if prev else None
            out.append(line)
            prev = "#"
            continue

        # For regular text, ensure a blank line before if the previous line is non-empty
        out.append("") if prev else None
        out.append(line)
        prev = "text"

    return "\n".join(out) + "\n"


def convert_md_to_pdf(
    md_text: str,
    template_path: Path,
    lua_filter_paths: list[Path] | Path,
) -> bytes:
    """
    Run Pandoc to convert markdown to PDF using the specified template and Lua filters.

    Args:
        md_text: Input markdown text.
        template_path: Path to the LaTeX template file.
        lua_filter_paths: List of paths to Lua filter files or a single path.

    Returns:
        PDF file content as bytes.
    """
    if isinstance(lua_filter_paths, Path):
        lua_filter_paths = [lua_filter_paths]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        pdf_path = tmpdir / "cv.pdf"

        # Convert Markdown to PDF using pypandoc
        try:
            pypandoc.convert_text(
                md_text,
                to="pdf",
                format="md",
                outputfile=str(pdf_path),
                extra_args=[
                    f"--template={template_path}",
                    "--pdf-engine=xelatex",
                ]
                + [f"--lua-filter={lf}" for lf in lua_filter_paths],
            )
        except RuntimeError as e:
            raise RuntimeError(f"Pandoc failed: {e}")

        return pdf_path.read_bytes()
