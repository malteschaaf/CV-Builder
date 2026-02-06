"""
CLI tool to generate a PDF CV from Markdown using Pandoc and Lua filters.
"""

import argparse
import base64
import os
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

# Import the markdown processing functions
from utils.markdown_processor import convert_md_to_pdf, preprocess_markdown


def generate_pdf(
    input_md: Path,
    output_pdf: Path,
    template: Path,
    lua_filters: list[Path],
    do_preprocess: bool = True,
    preview: bool = False,
):
    """
    Generate PDF from Markdown file using Pandoc.
    """
    if not input_md.exists():
        print(f"Error: Markdown file '{input_md}' does not exist.")
        sys.exit(1)

    md_text = input_md.read_text(encoding="utf-8")
    md_to_use = preprocess_markdown(md_text) if do_preprocess else md_text

    pdf_bytes = convert_md_to_pdf(md_to_use, template, lua_filters)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.write_bytes(pdf_bytes)
    print(f"✅ PDF generated at {output_pdf}")

    if preview:
        try:
            webbrowser.open(output_pdf.resolve().as_uri())
        except Exception as e:
            print(f"⚠️ Failed to open PDF preview: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate PDF CV from Markdown")
    parser.add_argument(
        "input_md",
        type=Path,
        nargs="?",
        default=Path("examples/default.md"),
        help="Input Markdown CV file (default: examples/default.md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/cv.pdf"),
        help="Output PDF file (default: output/cv.pdf)",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=Path,
        default=Path("templates/modern.tex"),
        help="LaTeX template to use",
    )
    parser.add_argument(
        "-f",
        "--filters",
        type=Path,
        nargs="*",
        default=[Path("filters/inline_dates.lua"), Path("filters/columns.lua")],
        help="List of Pandoc Lua filters",
    )
    parser.add_argument(
        "--no-preprocess",
        action="store_false",
        dest="do_preprocess",
        help="Disable automatic markdown preprocessing",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Open PDF in default viewer after generation",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    generate_pdf(
        input_md=args.input_md,
        output_pdf=args.output,
        template=args.template,
        lua_filters=args.filters,
        do_preprocess=args.do_preprocess,
        preview=args.preview,
    )


if __name__ == "__main__":
    main()
