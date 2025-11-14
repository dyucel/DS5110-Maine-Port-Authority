'''
Used for a text based PDF.
'''

# IMPORTS
from pypdf import PdfReader
import sys

# takes the second argument 
input_file = sys.argv[1]

# create a readable file object
reader = PdfReader(input_file)

# print the length of the document in pages
print(len(reader.pages))

# loop through all the pages, print the text
for i, page in enumerate(reader.pages):
    
    # print the page number
    print(f"\n--- Page {i + 1} ---")
    
    # extract the text on the page
    text = page.extract_text()
    
    # if not blank, print
    if text:
        print(text)
        
    # if blank, print the message
    else:
        print("(No text found on this page)")

