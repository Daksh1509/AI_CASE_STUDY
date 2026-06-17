# src/export_utils.py
"""Export case studies to Markdown and PDF."""
import os
from pathlib import Path
from src.config import CASE_STUDY_DIR

def save_markdown(content: str, company_name: str,
                  output_dir: str = CASE_STUDY_DIR) -> str:
    """Save case study as a .md file. Returns the file path."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    safe_name = company_name.replace(" ", "_").lower()
    filepath = os.path.join(output_dir, f"{safe_name}_case_study.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

def save_pdf(content: str, company_name: str,
             output_dir: str = CASE_STUDY_DIR) -> str:
    """Save case study as a .pdf file using FPDF2. Returns the file path."""
    try:
        from fpdf import FPDF
    except ImportError:
        raise ImportError("fpdf2 not installed. Run: pip install fpdf2")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    safe_name = company_name.replace(" ", "_").lower()
    filepath = os.path.join(output_dir, f"{safe_name}_case_study.pdf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for line in content.split("\n"):
        if line.startswith("# "):
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.cell(0, 10, line[2:], ln=True)
            pdf.set_font("Helvetica", size=11)
        elif line.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=13)
            pdf.cell(0, 8, line[3:], ln=True)
            pdf.set_font("Helvetica", size=11)
        else:
            pdf.multi_cell(0, 7, line)
    pdf.output(filepath)
    return filepath

def export_all(case_studies: dict, fmt: str = "md") -> dict:
    """Export all case studies. fmt = 'md' or 'pdf'."""
    paths = {}
    for company, content in case_studies.items():
        if fmt == "pdf":
            paths[company] = save_pdf(content, company)
        else:
            paths[company] = save_markdown(content, company)
    return paths
