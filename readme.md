# CV Builder – Markdown to PDF CV Generator

A minimalist, developer-friendly CV builder that converts clean Markdown into a beautifully typeset PDF using Pandoc, Lua filters, and LaTeX.

This project provides both a **Python CLI** and a **Streamlit web interface** for live editing and PDF generation. 
No account required, no tracking, no hidden state.

Write your CV like code.  
Render it like print.

---

## 🚀 Live App

You can access the live Streamlit application here:

👉 [CV Builder Live](https://cv-builder.streamlit.app)

---

## ✨ Key Features

- Write your CV in plain Markdown
- Convert Markdown CVs to **PDF** with LaTeX templates.
- **Multi-column support** for skills or bullet sections using `columns.lua`.
- Inline date formatting with `inline_dates.lua`.
- Streamlit interface for **live editing and preview**.
- Python CLI tool for **local PDF generation**.
- Automatic Markdown preprocessing for better Pandoc compatibility.

---

## 🧠 Philosophy

Most CV builders hide structure behind UI controls.

This project does the opposite:
- structure is explicit
- formatting is reproducible
- content is versionable

Your CV becomes:
- readable in Git
- diffable
- future-proof

---

## 📝 Writing Your CV

The CV is written in Markdown with a small YAML header for metadata.

Example structure:

```markdown
---
name: "Your Name"
email: "your@email.com"
phone: "+00 123456789"
linkedin: "linkedin.com/in/yourname"
address: "City, Country"
---

# YOUR ROLE OR TITLE
Short professional summary.

# EXPERIENCE
## Company Name
> Date Range

### Role Title
- Achievement or responsibility
- Another bullet point
```

---

## 📐 Multi-Column Sections (e.g. Skills)

To create multi-column layouts, use grouped bullet lists separated by horizontal rules.

Each bullet list becomes one column.

Example:

```markdown
# Skills

- Python, SQL, Julia
- Power BI, Snowflake

---

- Machine Learning
- Data Analysis

---

- Communication
- Problem Solving
```

This will render as multiple columns without bullet points.

---

## 🖥️ Local Development

### Requirements

- Python 3.9 or newer
- Pandoc
- XeLaTeX (TeX Live recommended)

### Install Dependencies

macOS:

```bash
brew install pandoc
brew install --cask mactex
```

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install pandoc texlive-xetex texlive-fonts-recommended
```

---

### Setup

Clone the repository:

```bash
git clone https://github.com/malte.schaaf/cv-builder.git
cd cv-builder
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

### Run the Streamlit App Locally

```bash
streamlit run app/app.py
```

Open your browser at:

http://localhost:8501

---

## 📄 Using the CLI Tool

To convert your Markdown CV to a pdf locally you can as well use the CLI Tool

### Generate PDF from Markdown

```bash
python -m cli.main generate examples/default.md -o output/cv.pdf
```

### Options

- `--no-preprocess` → disable Markdown auto-fixing  
- `--filters` → apply custom Lua filters  
- `--template` → specify a custom LaTeX template  
- `--preview` → open the generated PDF automatically  

Example:
```bash
python -m cli.main examples/my_cv.md -o output/my_cv.pdf --preview
```

---

## 📁 Project Structure

```bash
.
├── app/ # Streamlit web app
│ └── app.py
├── cli/ # CLI entrypoint
│ └── main.py
├── utils/ # Python utility functions
│ └── markdown_processor.py
├── filters/ # Pandoc Lua filters
│ ├── columns.lua
│ └── inline_dates.lua
├── templates/ # LaTeX templates
│ └── template.tex
├── examples/ # Default/example CVs
│ └── default.md
├── output/ # Generated PDFs
├── requirements.txt
└── README.md
```

---

## 🧩 How It Works

### CLI Tool

1. **Markdown Input** → can be your own `cv.md` or `examples/default.md`.
2. **Preprocessing** → optional fixes softbreaks, spacing, and formatting for Pandoc.
3. **Pandoc Conversion** → converts Markdown to LaTeX and applies Lua filters.
4. **PDF Generation** → XeLaTeX creates the final PDF.
5. **Preview / Output** → saves to `output/` and optionally opens for preview.

### Streamlit App

1. **Upload Your Markdown CV** → either upload your own `cv.md` file or start with the default example.  
2. **Edit Markdown** → modify the CV text in the editor provided in the app.  
3. **Auto-Fix Paragraph Breaks** → enable the checkbox to automatically adjust soft line breaks for proper Pandoc conversion.  
4. **Enable Lua Filters** → optionally apply filters like `inline_dates.lua` or `columns.lua`.  
5. **Generate PDF** → click the "Generate PDF" button to render the CV as a PDF.  
6. **Preview PDF** → after generation, the PDF is displayed in the app for review.  
7. **Download PDF** → click the download button to save the PDF locally.  
8. **Iterate Quickly** → make edits in Markdown, regenerate the PDF, and download again until satisfied.  

All steps are deterministic and reproducible.

---

## 🛣️ Roadmap

### Short-term
- Live PDF auto-refresh
- Better LaTeX error messages
- User-customizable LaTeX templates
- Export to other formats (HTML / DOCX) 

### Mid-term
- Multiple templates
- Template switching
- Improved mobile layout

### Long-term
- User Accounts
- Optional AI-assisted bullet rewriting
- Versioned CV exports
- Hosted PDF history

---

## 🔐 Security Notes

- No shell escape enabled
- No arbitrary LaTeX execution
- No data stored on the server
- Safe for personal CV data

---

## 📜 License

MIT License  
Free to use, modify, and distribute.

---

## 🙌 Credits

Built with:
- Pandoc
- Streamlit
- Lua
- XeLaTeX

**Core idea:**

A CV should be written like code — readable, versionable, and reproducible.
