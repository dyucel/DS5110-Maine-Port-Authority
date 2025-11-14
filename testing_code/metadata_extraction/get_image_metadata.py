# IMPORTS
import os
import sys
from PyPDF2 import PdfReader

# FUNCTIONS
def get_pdf_metadata(path):

    '''
    Parameter: full file path
    Returns: N/A

    Takes a file path as its only parameter, prints various attributes of the PDF. This uses metadata stored in the PDF's header, NOT file system meta data.
    '''
    
    try:
        reader = PdfReader(path)
        
    except Exception as e:
        print(f"ERROR: Could not open PDF — {e}")
        return

    metadata = reader.metadata
    
    if metadata:
        date = metadata.creation_date_raw
        print(f'...File Created: {date}')
        
    else:
        print("...No metadata found in this PDF!")

# MAIN
def main():

    input_directory = sys.argv[1]
    
    for file in os.listdir(input_directory):

        # skip whatever isn't a PDF
        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(input_directory, file)
        print(f'\nProcessing {file}...')
        get_pdf_metadata(path)

if __name__ == "__main__":
    main()
