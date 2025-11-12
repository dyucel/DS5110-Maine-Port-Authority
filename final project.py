import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# -----------------------------
# SETTINGS
# -----------------------------
input_dir = "pdf_files"              # Folder with PDFs
output_dir = "ocr_text_output"       # Folder to save extracted text
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# FUNCTIONS
# -----------------------------
def extract_text_pdfplumber(pdf_path):
    """Try to extract text directly using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text.strip()
    except Exception as e:
        print(f"pdfplumber failed for {os.path.basename(pdf_path)}: {e}")
        return ""

def ocr_pdf(pdf_path):
    """Convert each page to an image and perform OCR with progress feedback."""
    text = ""
    try:
        pages = convert_from_path(pdf_path, dpi=200)  # Poppler handles conversion
        total_pages = len(pages)
        print(f"Running OCR on {total_pages} pages...")
        for i, page in enumerate(pages, start=1):
            print(f"Processing page {i}/{total_pages} ...", end="\r")
            page_text = pytesseract.image_to_string(page, lang="eng")
            text += f"\n--- Page {i} ---\n{page_text}"
        print(f"Finished OCR for {os.path.basename(pdf_path)}")
        return text.strip()
    except Exception as e:
        print(f"OCR failed for {os.path.basename(pdf_path)}: {e}")
        return ""

# -----------------------------
# MAIN LOOP
# -----------------------------
for file in os.listdir(input_dir):
    if not file.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(input_dir, file)
    print(f"Processing {file}...")

    # Step 1: Try normal text extraction
    text = extract_text_pdfplumber(pdf_path)

    # Step 2: If no text, do OCR
    if len(text) < 100:
        print("Little or no text found — switching to OCR mode.")
        text = ocr_pdf(pdf_path)

    # Step 3: Save text to output folder
    if text:
        out_path = os.path.join(output_dir, file.replace(".pdf", ".txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f" Text saved: {out_path} ({len(text):,} characters)")
    else:
        print(f" No text extracted for {file}")
