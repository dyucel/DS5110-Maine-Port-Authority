# DS5110 – Maine Port Authority Document Automation

This repository contains an automated pipeline developed as a final project for DS5110, in order to process, rename, categorize, and extract metadata from documents (PDF, DOCX, TXT) from the Maine Port Authority. Our goal was to create an automated document-management workflow that:

* Extracts text from documents (including scanned/unreadable PDFs via OCR),
* Renames files using meaningful labels (most frequent word/phrase + date),
* Groups documents into folders based on cosine-similarity scores,
* Extracts metadata such as creation dates,
* Outputs a cleaned, organized folder structure suitable for long-term use.

Files used can be accessed here: https://drive.google.com/drive/folders/110S6NpFZ322YgzaI3mQ3imQOysZoCPdF?usp=drive_link

## Project Overview

Many documents provided to us were not directly readable by Python because they were scanned PDFs/not text-extractable. As a result, our scripts integrate several text-extraction strategies as necessary. After text extraction, files are renamed, clustered, and reorganized using cosine similarity, and metadata is extracted.

### 1. Text Extraction (extractwsubfolders.py)

This script performs all PDF text extraction for the pipeline and was designed to handle the highly mixed document quality of the Maine Port Authority archive. The extraction process uses two stages: a fast direct extraction and a fallback OCR pipeline. 

#### A. Collecting Files From Nested Folders

Before extraction, the script provides counts of PDF and DOCX files, and then:
Recursively scans the entire raw_files/ directory
Copies all .pdf files to pdf_files_up/

Copies all .docx files to docx_files_up/
This ensures the program can process deeply nested client folders without manual cleanup. 

#### B. Direct Text Extraction (pdfplumber)

For each PDF:

Attempt to extract text using pdfplumber.
If the output contains ≥ 100 characters, the script treats the file as a digital PDF.
The text is saved immediately with no OCR needed.
This threshold avoids unnecessary OCR for clean, digital documents and significantly speeds up processing. 

#### C. OCR Extraction (Tesseract) for Scanned PDFs

If a PDF contains little or no extractable text:

Convert each page to an image using pdf2image (Poppler backend)
Run Tesseract OCR (via pytesseract) page by page
Print detailed progress updates (e.g., “Processing page 3/56…”)

Save the extracted text into a .txt file that mirrors the PDF’s original base name
Example: Lease-2019.pdf → Lease-2019.txt

This consistency is critical for the renaming and cosine similarity grouping steps.  

#### D. Output

All extracted text—whether from pdfplumber or OCR—is saved into:
ocr_text_output_2/

Each file retains the same base name as its original PDF, ensuring a 1:1 mapping used by the renaming and grouping modules.

### 2. Metadata Extraction (extract_metadata.py)

Our program focuses on two main types of files: PDFs and DOCX. Both of these file types contain embedded, document-level metadata, but require different libraries to access. They are detailed as follows:

1. .pdf

    More information available here regarding the library: https://pypdf2.readthedocs.io/en/3.x/modules/DocumentInformation.html
    
    This code extracts the embedded metadata available in a file.
    
    We can access the following properties that are part of nearly every PDF file:
    
    ...File Author (str)
    ...File Creation Date (datetime)
    ...File Creator (str)
    ...File Modified Date (datetime)
    ...File Producer (str)
    ...File Subject (str)
    ...File Title (str)

   Each value actually consists of two properties: standard and a "raw" version, which always returns a TextStringObject.

2. .doc
   
    More information available here regarding the library: https://python-docx.readthedocs.io/en/latest/dev/analysis/features/coreprops.html

   We can access the following properties that are part of nearly every DOCX file:

   ...author (unicode)
   ...category (unicode)
   ...comments (unicode)
   ...content_status (unicode)
   ...created (datetime)
   ...identifier (unicode)
   ...keywords (unicode)
   ...language (unicode)
   ...last_modified_by (unicode)
   ...last_printed (datetime)
   ...modified (datetime)
   ...revision (int)
   ...subject (unicode)
   ...title (unicode)
   ...version (unicode)

### 3. File Renaming (documenttitling2.py)

This script attempts to find a suitable date and WIN number associated with the documents in a folder and add it to the beginning of the file name.
It prioritizes leaving document names the same as they are if there is a detectable date already in the title or if no suitable date/WIN number can be found.
Legacy functionality that attempts to rename the document based on the text in the document is still available by changing the function call found currently on line 282 from

        dictionary =generate_title_dictionary_2(path) ----> dictionary =generate_title_dictionary(path)

The main function of the file takes in up to 2 arguments. The first is mandatory, being the file path to a folder that contains .docx and .txt files that should be renamed. The second argument
is optional, and should the file path to any pdf's that had their text extracted from them and placed into .txt files in the first folder. This will allow the program to rename the pdf's as well
with the same name as their assocated .txt files.

Methods in this script:
    getText(filename)
        Extracts text from a .docx with filename as it's file path. Returns list that is the split of the text in the .docx file

    find_dates(list)
        Given a list that is the split of the text to be analyzed, it will obtain all decipherable month/date pairs that appear with 5 spots in the list from each other. 
        Creates a dictionary of each decipherable pair and a list of each location of their occurance in the argument list. Sorts this by the size of each list and returns the dictionary

    generate_name(text_entered, freq_dict_entered, bifreq_dict_entered)
        Legacy function that attempts to create a new name for a document from it's text as a list (text_entered), it's frequency list of that text (freq_dict_entered), and the
        bifrequency list of that text(bifreq_dict_entered). It analyzes the two frequency lists for matches to generate a seed word. Then creates a title from the 
        2 words before the seed word and the 10 words after in the text. Will use find_dates to get a date to attach to the title as well. Returns a string name 

    generate_name_2(text_entered, old_name)
        Function to generate a new name for a document based on the text of the document as a list (text_entered), and the string old_name of the document. First attempts to find any
        dates already in the document title. If it does, it skips trying to find a date in the document. Otherwise, uses the find_dates method to get a date. Then attempts to find a
        labeled WIN number in the document. Attempts to rename the document using the WIN number and date if any attached to the start. Returns the new name created

    gen_freq_dicts(text_whole)
        Function to generate frequency dictionary and bifrequency dictionary from the split list of text in the document. First, pares down the text given to only be alphanumeric. Also excludes words
        that are under 2 in length and over 14 in an attempt to reduce unreadable words. Then from the text list generates the frequency dictionary and bifrequency dictionary and sorts it based on number
        of occurances. Returns both dictionaries

    generate_title_dictionary_2(folder_path)
        Iterates through all files in folder_path and extracts text from them. Uses generate_name_2 to create a new name for the document and stores old_name:new_name in a dictionary. Returns the dictionary at the end
        
    generate_title_dictionary(folder_path)
        Legacy function to generate a dictionary of titles. Iterates through all files in folder_path and extracts text from them. Uses gen_freq_dicts to generate the frequency dictionaries and passes them to
        generate_name to create new name. Stores each old_name:new_name pair in a dictionary.

    rename_files(title_dictionary, file_path, pdf_file_path)
        Function that takes in a generated title dictionary, a file_path that is a folder that contains all the .docx/.txt files to be renamed, and pdf_file_path that is the file
        path to the folder that contains all the pdf files assocated with any .txt files. Pass an empty string for pdf_file_path if there is no such folder. Iterates through the title_dictionary and 
        renames any relevant files in file_path or pdf_file path with the new names.
        
    main(path, pdf_path="")
        Main function. Pass string path that is the file path to the folder that contains any .docx or .txt files to be renamed. Pass string pdf_path that contains any .pdf files that are associated with .txt files in path.
        This defaults to the empty string if no such path. Renames any files in path and pdf_path that have dates or WIN numbers found in the text of them that don't already have them in the document title.


### 4. Document Organization (organizer2.py)
This script groups documents into coherent, topic-based clusters using semantic similarity. It operates after text extraction and renaming, relying on cleaned text to determine which documents belong together.

#### A. Loading Document Text

The script loads text from all available processed files:

* TXT files generated from PDFs (via direct extraction or OCR)

* DOCX files using python-docx

* Files are skipped if they contain too little usable text (e.g., scanned maps, images, or extraction failures).

#### B. Cleaning the Text

Before computing embeddings, each document’s text is standardized:

* Lowercasing, removing OCR noise (page markers, stray characters, symbols), and removing punctuation

* Discarding files with fewer than ~20 meaningful words

This ensures that embeddings capture meaningful content rather than noise.

#### C. Embedding & Similarity Computation

The script converts all documents into numerical vectors using "all-MiniLM-L6-v2" (SentenceTransformer).

Then it computes pairwise cosine similarity between all documents.
Cosine similarity provides a continuous measure of how similar two documents are in meaning.

#### D. Forming High-Confidence Initial Pairs

To identify strong connections early on, the script:

* Finds the strongest match for each document

* Creates a pair only if similarity ≥ 0.8 (can be changed)

* Uses these pairs as seed groups that form the backbone of the final clusters

These initial pairs represent documents that are extremely close in content and, therefore, safe to group immediately.

#### E. Iterative Assignment of Remaining Files

After seed groups are created, the algorithm assigns the rest of the documents, for each ungrouped file:

* Compute its average cosine similarity to each existing group.

* Assign it to the group with the highest mean similarity.

* Repeat until all files are processed.

If a file’s best similarity is below 0.2, a new single-file group is created. This hybrid strategy combines strong early pairs with flexible clustering for weaker matches.

#### F. Automatically Naming Each Group

To give each folder an interpretable name, the script:

* Collects the final filenames inside the group

* Extracts frequent, meaningful keywords (ignoring very short words)

* Picks the most common informative word as the cluster label

* Detects the first year-like pattern (e.g., 2018, 2021) and adds it to the name when present

This produces group names such as:

"Logistics_2019"
"Contracts_2021"
"Terminal_20"

#### G. Exporting Final Organized Folders

For every group:

* A new folder is created under organized_folders_final/

* All corresponding PDF and DOCX files are copied into the folder

* Original filenames and extensions are preserved

* TXT files are used only for grouping, not exported

This results in a clean, searchable, topic-based folder system.

### Why TXT Files Are Used for PDFs

TXT files contain the best extracted text from the PDFs (whether via pdfplumber or OCR). Since PDFs vary in structure and quality, TXT files provide a standardized, reliable text format for computing document similarity. DOCX files, on the other hand, supply their own text directly.

## Notes & Limitations

A small portion of the PDFs cannot be processed fully, typically because they are corrupted, extremely low-quality scans, or image-only documents containing almost no text. In practice, this is expected when working with large, heterogeneous file collections and does not meaningfully affect the overall clustering results for the larger sample. Even when OCR succeeds, its output can introduce misread characters, spacing issues, and leftover page markers, which the cleaning portion of the code reduces but cannot eliminate. Some documents may still carry imperfect or incomplete textual representations into the similarity model.

Additionally, very long or multi-topic files can have several categories at once, making their similarity scores less decisive. Embedding models capture meaning quite well, but they can still struggle with documents that shift topics or combine unrelated material, occasionally leading to ambiguous or imperfect group assignments.

Finally, the similarity thresholds used in this project, high-confidence pairing at 0.8 and minimum assignment at 0.2, work well for this dataset but are not universal. Different collections may require tuning depending on document length, OCR quality, and overall topic diversity. The workflow is also computationally heavy: OCRing many long PDFs and generating embeddings for every file takes both time and processing power. These constraints are not unencountered in large-scale document organization, and they seem to be manageable within the overall pipeline.
    


   
