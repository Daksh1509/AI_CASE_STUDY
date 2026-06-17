# app/streamlit_app.py
"""Streamlit UI for AI Case Study Generator."""
import streamlit as st
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.input_loader import load_file
from src.preprocess import clean_text
from src.chunker import chunk_text
from src.summarizer import summarize_document
from src.insight_extractor import extract_insights
from src.references import extract_all_references, flatten_references
from src.generator import generate_case_study
from src.export_utils import save_markdown, save_pdf

st.set_page_config(
    page_title="AI Case Study Generator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI-Powered Case Study Generator")
st.markdown("Upload documents for a company and generate a structured AI case study.")

with st.sidebar:
    st.header("⚙️ Settings")
    company_name = st.text_input("Company Name", value="Company A")
    export_format = st.radio("Export Format", ["Markdown", "PDF"])
    max_summary_len = st.slider("Max Summary Length (words/chunk)", 50, 300, 150)
    st.divider()
    st.caption("Supported formats: .pdf, .docx, .txt")

st.header("📤 Upload Documents")
uploaded_files = st.file_uploader(
    "Upload company documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if st.button("⚡ Generate Case Study", type="primary") and uploaded_files:
    all_text = ""
    with st.spinner("Loading and preprocessing documents..."):
        for uploaded_file in uploaded_files:
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            raw_text = load_file(tmp_path)
            all_text += clean_text(raw_text) + "\n"
            os.unlink(tmp_path)

    with st.spinner("Summarizing..."):
        summary = summarize_document(all_text)

    with st.spinner("Extracting insights..."):
        insights = extract_insights(summary)

    with st.spinner("Extracting references..."):
        refs = flatten_references(extract_all_references(all_text))

    with st.spinner("Generating case study..."):
        case_study_md = generate_case_study(
            company_name=company_name,
            summary=summary,
            insights=insights,
            references=refs
        )

    st.success("✅ Case study generated!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Case Study Preview")
        st.markdown(case_study_md)

    with col2:
        st.subheader("💡 Insights Breakdown")
        for category, items in insights.items():
            if items:
                st.markdown(f"**{category.title()}**")
                for item in items:
                    st.markdown(f"- {item}")

    st.divider()
    st.subheader("📥 Download")
    if export_format == "PDF":
        pdf_path = save_pdf(case_study_md, company_name)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=f"{company_name}_case_study.pdf")
    else:
        st.download_button(
            "Download Markdown",
            case_study_md,
            file_name=f"{company_name}_case_study.md",
            mime="text/markdown"
        )
elif not uploaded_files:
    st.info("👆 Upload at least one document and click Generate.")
