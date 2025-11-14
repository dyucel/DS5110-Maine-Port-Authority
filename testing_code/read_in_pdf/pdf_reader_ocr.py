'''
Used for a non-text based PDF.
'''

# IMPORTS
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import sys

# takes the second argument 
pdf_path = sys.argv[1]

# first try to convert a PDF to an image
try:
    
    # convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=300)
    
    # loop through each page image and extract text
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)

        # if not blank, print
        if text:
            print(text)

        # if blank, print the message
        else:
            print("(No text found on this page)")

# no file found, print error
except FileNotFoundError:
    print(f"Error: File not found at {pdf_path}")

# tesseract not installed
except pytesseract.TesseractNotFoundError:
    print("Error: Tesseract OCR engine not found. Please install it and add to PATH.")

# other error
except Exception as e:
    print(f"An error occurred: {e}")

