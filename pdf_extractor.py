import fitz  # PyMuPDF
import pdfplumber
import camelot
import json
import os
import sys

def extract_text_blocks(pdf_path):
    """Extracts paragraphs and headings using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)
    pages_content = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        content = []
        for b in blocks:
            text = b[4].strip()
            if not text:
                continue

            # Very simple heuristic: ALL CAPS = section header
            if text.isupper() and len(text.split()) < 8:
                content.append({
                    "type": "paragraph",
                    "section": text,
                    "sub_section": None,
                    "text": ""
                })
            else:
                content.append({
                    "type": "paragraph",
                    "section": None,
                    "sub_section": None,
                    "text": text
                })

        pages_content.append({"page_number": page_num, "content": content})
    return pages_content


def extract_tables(pdf_path):
    """Extract tables using Camelot (works best on lattice PDFs)."""
    tables_by_page = {}
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")
        for t in tables:
            page = t.page
            if page not in tables_by_page:
                tables_by_page[page] = []
            tables_by_page[page].append({
                "type": "table",
                "section": None,
                "description": None,
                "table_data": t.df.values.tolist()
            })
    except Exception as e:
        print("Table extraction error:", e)
    return tables_by_page


def parse_pdf(pdf_path, output_json="output.json"):
    pages_content = extract_text_blocks(pdf_path)
    tables_by_page = extract_tables(pdf_path)

    for page in pages_content:
        if page["page_number"] in tables_by_page:
            page["content"].extend(tables_by_page[page["page_number"]])

    output = {"pages": pages_content}

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py <input.pdf> [output.json]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else "output.json"

    result = parse_pdf(pdf_file, json_file)
    print(f"✅ JSON saved to {json_file}")
